---
title: Remote Management: SSH and paramiko
summary: How to run commands on remote servers over SSH from Python and copy files via SFTP using the paramiko library.
order: 5
duration: 40 min
difficulty: advanced
tags: SSH, paramiko, SFTP, servers, remote management
---

## Why Python should speak SSH

Developers and DevOps engineers constantly work with remote servers: updating code, restarting services, checking logs, collecting statistics. By hand this is done through a terminal and SSH. But when there are dozens of servers and the commands repeat, SSH sessions are automated from Python.

The **paramiko** library is a pure-Python implementation of the SSH protocol. It lets you connect to servers, run commands, and work with files over SFTP. Install it with `pip install paramiko`.

## Connecting and running a simple command

A minimal example: connect and run `uname -a` (system information):

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("192.168.1.50", username="deploy", password=[redacted])

stdin, stdout, stderr = client.exec_command("uname -a")
print(stdout.read().decode())
client.close()
```

Let's go step by step. `SSHClient()` creates a client. `set_missing_host_key_policy(paramiko.AutoAddPolicy())` automatically adds unknown host keys — handy for scripts, but in production it's better to verify keys with `RejectPolicy` (the default) and pre-register known ones. `connect` opens a connection. `exec_command` runs a command and returns three streams: stdin, stdout, stderr. `stdout.read()` reads all the output, and `.decode()` turns bytes into a string. Always `close()` at the end.

## Reading errors

A command may finish with an error. It's useful to check the exit code:

```python
stdin, stdout, stderr = client.exec_command("ls /nonexistent")
exit_status = stdout.channel.recv_exit_status()
print("Exit code:", exit_status)
print("Error:", stderr.read().decode())
```

`stdout.channel.recv_exit_status()` waits for the command to finish and returns its exit code. That's how we tell success (0) from failure.

## Working with files: SFTP

SFTP is a subprotocol of SSH for transferring files. With paramiko you get it from the same connection:

```python
sftp = client.open_sftp()
sftp.get("/var/log/app.log", "app_local.log")   # download
sftp.put("config.yaml", "/srv/app/config.yaml")  # upload
sftp.close()
```

`get` downloads a file from the server, `put` uploads one to the server. The `sftp` object also knows `listdir`, `stat`, `mkdir`, `remove` — almost everything a regular file manager does.

## Handling connection errors

The network is unreliable: the server may be down, the password may be wrong. Always wrap the connection in `try/except`:

```python
try:
    client.connect(host, port=22, username=user, password=pwd, timeout=10)
except paramiko.AuthenticationException:
    print("Authentication failed")
except paramiko.SSHException as e:
    print("SSH error:", e)
except TimeoutError:
    print("Connection timed out")
```

`AuthenticationException` — wrong login or password; `SSHException` — other protocol problems; `TimeoutError` — the server isn't responding. A good script always reports exactly what went wrong.

## Security

Passwords in code are bad practice: everyone with access to the repository will see them. Better to use SSH keys (the `key_filename` parameter), environment variables, or secret managers. In the examples below we use a password from a variable for simplicity, but in production — keys.

## The path of a single command

Any SSH automation breaks down into the same set of steps — from connecting to closing the channel.

```mermaid
flowchart LR
    A["Script"] --> B["SSHClient.connect"]
    B --> C["exec_command"]
    C --> D["stdout and exit code"]
    D --> E["open_sftp"]
    E --> F["get or put"]
    F --> G["close"]
```

## Summary

We learned to connect over SSH, run commands, read their output and errors, and transfer files via SFTP. That's the foundation for deployment and administration scripts. Now the tasks.

<!--TASK-->
### Task 1
Write a script `ssh_uptime.py` that connects to a server (address `192.168.1.50`, user `deploy`, password `secret`) and runs the command `uptime`. Print the command output to the screen. Use `SSHClient`, `AutoAddPolicy`, and `exec_command`. Don't forget to close the connection with `client.close()` at the very end.

### Task 2
Create a script `ssh_status.py` that runs the command `service nginx status` on the server and prints both the output and the exit code (via `stdout.channel.recv_exit_status()`). If the exit code is not zero, additionally print the message `Service is not running!`. Test the behavior on a definitely absent service (for example, `service ghost-service status`) to see a non-zero code.

### Task 3
Write a script `sftp_download.py` that downloads the file `/var/log/app.log` from the server to the local file `app.log` via `sftp.get()`. Before downloading, print the remote file size via `sftp.stat("/var/log/app.log").st_size`. Wrap the connection in `try/except`, catching `paramiko.AuthenticationException`, `paramiko.SSHException`, and `TimeoutError`.

### Task 4
Create a script `sftp_upload.py` that uploads the local file `backup.tar.gz` to the server at `/srv/backups/backup.tar.gz` via `sftp.put()`. Before uploading, create the remote folder `/srv/backups` if it doesn't exist: check with `try: sftp.stat(...)` and create with `sftp.mkdir(...)`, catching `FileNotFoundError`.

### Task 5
Write a script `multi_host.py` that runs the command `hostname` on three servers from the list `[("192.168.1.50", "deploy", "secret"), ("192.168.1.51", "deploy", "secret"), ("192.168.1.52", "deploy", "secret")]` and prints for each: the address and the command result. If connecting to some server fails — print `Could not connect to <address>`, but continue working with the rest. Use a loop and `try/except` around the connection.

### Task 6
Write a function `disk_usage(client, threshold=80)` that runs the command `df -h /` on the server, reads stdout, and parses the output. Find the usage percentage with the regular expression `(\d+)%`, return the tuple `(percent, status)`, where `status` is `"ALERT"` if the percentage is greater than or equal to the threshold, otherwise `"OK"`. If the output is empty or the percentage is not found — return `(None, "UNKNOWN")`. Test the function on a stub client: a class with an `exec_command` method that returns prepared output via `io.BytesIO`. This way the test doesn't depend on a live server. Expected output for the line `78% /` with threshold 80: `(78, 'OK')`, and with threshold 75: `(78, 'ALERT')`.

### Task 7
Write a script `sync_conf.py` that copies all `*.conf` files from the local directory `conf/` to `/etc/app/conf/` on the server. For each file, compare its size with the remote one (`sftp.stat(remote).st_size`): if the sizes match — skip the file, otherwise upload it via `sftp.put`. If the remote directory is missing (stat raises `FileNotFoundError`) — create it via `sftp.mkdir`. At the end print `Uploaded: N, skipped: M`. Run the script twice: the first run should upload all three files, the second — none. Expected output: `Uploaded: 3, skipped: 0`, then `Uploaded: 0, skipped: 3`.

<!--/TASK-->

<!--HINT-->
### Hint 1
Create the client: `client = paramiko.SSHClient()`, then `client.set_missing_host_key_policy(paramiko.AutoAddPolicy())`. Connect: `client.connect("192.168.1.50", username="deploy", password=[redacted])`. Print: `print(stdout.read().decode())`.

### Hint 2
After `exec_command`, wait for completion: `exit_status = stdout.channel.recv_exit_status()`. Then compare `if exit_status != 0:`. Don't forget to read stderr — that's usually where the cause of the error is.

### Hint 3
SFTP session: `sftp = client.open_sftp()`. File size: `sftp.stat(path).st_size`. Download: `sftp.get(remote, local)`. Close both `sftp` and `client`. `TimeoutError` is a built-in exception — no need to import it.

### Hint 4
Check folder existence: `try: sftp.stat("/srv/backups") except FileNotFoundError: sftp.mkdir("/srv/backups")`. Then `sftp.put("backup.tar.gz", "/srv/backups/backup.tar.gz")`.

### Hint 5
In a loop `for host, user, pwd in hosts:` wrap `connect` in `try/except Exception as e:` — inside `except` print a message and continue via `continue`. On success — print the result. Close the client after each server.

### Hint 6
The stub should mimic only the slice of the API that the function uses: `def exec_command(self, cmd): return None, io.BytesIO(self.output.encode()), io.BytesIO(b"")`. In the function itself read `stdout.read().decode()`, search `re.search(r"(\d+)%", output)`, and check `if not m`. Compare the threshold non-strictly: `percent >= threshold`, otherwise exactly 80% with threshold 80 would not trigger an alert — and that's already a reason to watch the disk.

### Hint 7
Keep the two checks separate: `sftp.stat(REMOTE_DIR)` for the directory and `sftp.stat(remote)` for each file — in the second case, `FileNotFoundError` means "the file doesn't exist yet", not an error. Local file size — `local.stat().st_size`. Increment the counters in the `continue` branch and after `put`. Don't forget to close `sftp`, then `client`.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("192.168.1.50", username="deploy", password=[redacted])

stdin, stdout, stderr = client.exec_command("uptime")
print(stdout.read().decode())

client.close()
```

Output (example):

```
 10:45:02 up 42 days,  3:20,  1 user,  load average: 0.08, 0.12, 0.15
```

What's happening here? `SSHClient` is a connection manager. `set_missing_host_key_policy(AutoAddPolicy())` says: if the host is unknown, add its key automatically — this saves you from having to register each server manually (in production `RejectPolicy` with an explicit list of known keys is better). `exec_command` doesn't wait for the command to finish by itself — it only launches it in a channel, so we read `stdout.read()`, which blocks until the command completes. `.decode()` turns bytes into a string. `close()` closes the connection — that's important, otherwise the script will leave "hanging" connections.

### Solution 2
Solution:

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("192.168.1.50", username="deploy", password=[redacted])

stdin, stdout, stderr = client.exec_command("service nginx status")
exit_status = stdout.channel.recv_exit_status()

print("Output:", stdout.read().decode())
print("Exit code:", exit_status)
if exit_status != 0:
    print("Error:", stderr.read().decode())
    print("Service is not running!")

client.close()
```

What's happening here? The command `service ... status` returns 0 if the service is running and a non-zero code otherwise. `recv_exit_status()` blocks until the command finishes and returns its exit code — the analogue of `$?` in bash. Then we check the code and, if it's not zero, print stderr and a message. Important: stdout and stderr can be read after `recv_exit_status` or before — both work, but changing the order can affect how much data is buffered. For short commands the output is read in full.

### Solution 3
Solution:

```python
import paramiko

REMOTE = "/var/log/app.log"
LOCAL = "app.log"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect("192.168.1.50", username="deploy", password=[redacted], timeout=10)
    sftp = client.open_sftp()
    size = sftp.stat(REMOTE).st_size
    print(f"Remote file size: {size} bytes")
    sftp.get(REMOTE, LOCAL)
    print(f"Downloaded to {LOCAL}")
    sftp.close()
except paramiko.AuthenticationException:
    print("Authentication failed")
except paramiko.SSHException as e:
    print("SSH error:", e)
except TimeoutError:
    print("Connection timed out")
finally:
    client.close()
```

What's happening here? `timeout=10` limits the connection wait to 10 seconds. `sftp.stat(REMOTE).st_size` gives the file's size on the server without downloading it. `sftp.get` performs the transfer. The `except` block catches three characteristic errors: wrong credentials, any protocol errors, and a timeout. `finally` guarantees the connection closes even on an error. This pattern is the standard for network-working scripts: the network is unreliable, and the program shouldn't crash with a cryptic traceback.

### Solution 4
Solution:

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("192.168.1.50", username="deploy", password=[redacted])

sftp = client.open_sftp()
try:
    sftp.stat("/srv/backups")
except FileNotFoundError:
    sftp.mkdir("/srv/backups")
    print("Created folder /srv/backups")

sftp.put("backup.tar.gz", "/srv/backups/backup.tar.gz")
print("File uploaded")
sftp.close()
client.close()
```

What's happening here? `sftp.stat` checks whether the remote folder exists: if it doesn't, paramiko raises `FileNotFoundError` (the same exception as in Python when working with local files — that's convenient). We catch it and create the folder with `sftp.mkdir`. Then `sftp.put` uploads the local file to the server. Notice the closing order: first `sftp`, then `client`. In production, instead of a hard-coded password, it's better to pass `key_filename="/home/deploy/.ssh/id_ed25519"` — then you don't have to store the password in code.

### Solution 5
Solution:

```python
import paramiko

hosts = [
    ("192.168.1.50", "deploy", "secret"),
    ("192.168.1.51", "deploy", "secret"),
    ("192.168.1.52", "deploy", "secret"),
]

for host, user, pwd in hosts:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=pwd, timeout=5)
        stdin, stdout, stderr = client.exec_command("hostname")
        print(f"{host}: {stdout.read().decode().strip()}")
    except Exception as e:
        print(f"Could not connect to {host}: {e}")
    finally:
        client.close()
```

Output (example):

```
192.168.1.50: web-01
192.168.1.51: web-02
192.168.1.52: db-01
```

What's happening here? The `hosts` list contains "address, login, password" tuples. The loop goes through all servers: for each one we create a separate client (important — connections can't be reused across different hosts). `try/except Exception` catches any connection error (unreachable host, wrong password) and prints the address with the reason, without stopping the whole script. `finally` closes the client in any case. Such a script is the basis for "sweeping" a fleet of servers: you can add any command here and get a report for all machines.

### Solution 6
Solution:

```python
import io
import re

def disk_usage(client, threshold=80):
    stdin, stdout, stderr = client.exec_command("df -h /")
    output = stdout.read().decode()
    m = re.search(r"(\d+)%", output)
    if not m:
        return (None, "UNKNOWN")
    percent = int(m.group(1))
    status = "ALERT" if percent >= threshold else "OK"
    return (percent, status)

class FakeClient:
    """Stub: returns a pre-prepared command output."""
    def __init__(self, output):
        self.output = output

    def exec_command(self, cmd):
        return None, io.BytesIO(self.output.encode()), io.BytesIO(b"")

df_output = (
    "Filesystem      Size  Used Avail Use% Mounted on\n"
    "/dev/sda1        50G   39G  8.6G  78% /\n"
)
client = FakeClient(df_output)
print(disk_usage(client, 80))
print(disk_usage(client, 75))
```

Output:

```
(78, 'OK')
(78, 'ALERT')
```

What's happening here? `exec_command` returns three streams, but we only need stdout; we read it fully and decode from bytes to a string. The regular expression `(\d+)%` looks for the number before the percent sign and captures it into a group — `int(m.group(1))` gives the ready value. From `df -h`, the percentage comes rounded, so don't expect precision to a tenth: for a threshold alert that's enough. If the command returns an unexpected format (different locale, different filesystem), `re.search` returns `None`, and the function honestly says `UNKNOWN` instead of crashing with `AttributeError`. The `FakeClient` class is an important part of the solution: it mimics only `exec_command`, so the test needs neither a network, nor a server, nor the paramiko library when checking the logic.

### Solution 7
Solution:

```python
from pathlib import Path
import paramiko

REMOTE_DIR = "/etc/app/conf"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(
    "192.168.1.50",
    username="deploy",
    key_filename=str(Path.home() / ".ssh" / "id_ed25519"),
    timeout=10,
)
sftp = client.open_sftp()

try:
    sftp.stat(REMOTE_DIR)
except FileNotFoundError:
    sftp.mkdir(REMOTE_DIR)

uploaded = 0
skipped = 0

for local in Path("conf").glob("*.conf"):
    remote = f"{REMOTE_DIR}/{local.name}"
    try:
        remote_size = sftp.stat(remote).st_size
    except FileNotFoundError:
        remote_size = None
    if remote_size == local.stat().st_size:
        skipped += 1
        continue
    sftp.put(str(local), remote)
    uploaded += 1

print(f"Uploaded: {uploaded}, skipped: {skipped}")
sftp.close()
client.close()
```

Output over two runs:

```
Uploaded: 3, skipped: 0
Uploaded: 0, skipped: 3
```

What's happening here? The script goes through local `*.conf` files and builds a remote path for each. Checking the size is a cheap way to see if a file changed: if the sizes match, the content is almost certainly the same, and traffic isn't wasted. `FileNotFoundError` in the inner `try` means "the file doesn't exist on the server yet", so `remote_size` becomes `None`, the condition doesn't fire, and the file is uploaded. The separate directory check is needed once: `mkdir` without it would fail if the folder already exists. The counters separate the two outcomes, and the report immediately shows whether it was a first run or a repeat. Authentication goes by key via `key_filename` — unlike a password in code, the key doesn't end up in the repository. We close `sftp` first, then `client`: the session lives inside the connection.

<!--/SOLUTION-->

<!--QUIZ-->
Which paramiko method runs a command on the server?
- exec_command
- run_command
- execute
* Correct answer: exec_command
exec_command launches a command in an SSH channel and returns stdin, stdout, stderr.

What does set_missing_host_key_policy(AutoAddPolicy()) do?
- Adds unknown host keys automatically
- Disables key verification
- Forbids connections to new hosts
* Correct answer: Adds unknown host keys automatically
AutoAddPolicy trusts new hosts without confirmation.

How to get a command's exit code in paramiko?
- stdout.channel.recv_exit_status()
- stderr.read()
- client.returncode
* Correct answer: stdout.channel.recv_exit_status()
recv_exit_status() waits for completion and returns the exit code.

Which SFTP method downloads a file from the server?
- sftp.get()
- sftp.put()
- sftp.download()
* Correct answer: sftp.get()
get(remote, local) downloads a file from the server to the local machine.

Which error will paramiko raise on a wrong password?
- paramiko.AuthenticationException
- paramiko.SSHException
- TimeoutError
* Correct answer: paramiko.AuthenticationException
AuthenticationException signals authentication problems.

What does exec_command return?
- Three streams: stdin, stdout, stderr
- A single string with output
- The exit code
* Correct answer: Three streams: stdin, stdout, stderr
Unpack as: stdin, stdout, stderr = client.exec_command("cmd").

Which SFTP method uploads a file to the server?
- sftp.put()
- sftp.get()
- sftp.send()
* Correct answer: sftp.put()
put(local, remote) uploads a local file to the server; get downloads.

Which exception will paramiko raise when a server is unreachable (timeout)?
- TimeoutError
- paramiko.AuthenticationException
- FileNotFoundError
* Correct answer: TimeoutError
If the server doesn't respond within the allotted time, TimeoutError is raised.

What will stdout.read() return if the command printed nothing?
- b""
- None
- An empty string str
* Correct answer: b""
read() returns bytes, so empty output is b"", not None.

Why specify timeout in client.connect()?
- So the connection doesn't hang forever on a dead server
- So the command runs longer
- To disable host key verification
* Correct answer: So the connection doesn't hang forever on a dead server
Without a timeout the script can wait a very long time for an unreachable host.

What does sftp.listdir(path) do?
- Returns a list of file names in the directory
- Downloads the whole directory
- Deletes the directory
* Correct answer: Returns a list of file names in the directory
This is the analogue of os.listdir for a remote filesystem.

What is preferable to a password in code for SSH automation?
- An SSH key via key_filename
- root login with a simple password
- Disabling host key verification
* Correct answer: An SSH key via key_filename
A key isn't stored in the repository and doesn't get into commit history.
<!--/QUIZ-->
