---
title: Wi-Fi and HTTP on MicroPython
summary: Connect, requests, urequests.
order: 3
duration: 45 min
difficulty: advanced
tags: wifi, http, micropython
---

Devices talk to the internet.

## Connect

```python
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "password")
while not wlan.isconnected():
    pass
print(wlan.ifconfig())
```

## HTTP

```python
import urequests
resp = urequests.get("https://httpbin.org/get")
print(resp.json())
resp.close()
```

## Lesson summary

network module connects; urequests sends HTTP.

<!--TASK-->
### Task 1 — Connect
Connect to Wi-Fi.

### Task 2 — Wait
Wait until connected.

### Task 3 — IP
Print the IP.

### Task 4 — Get
Fetch a URL.

### Task 5 — Close
Close the response.

### Task 6 — Post
Send a POST.

### Task 7 — Error
Handle connection failure.
<!--/TASK-->

<!--HINT-->
### Hint 1
WLAN.

### Hint 2
isconnected.

### Hint 3
ifconfig.

### Hint 4
urequests.

### Hint 5
close().

### Hint 6
post().

### Hint 7
Try.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "password")
```

### Solution 2
```python
while not wlan.isconnected():
    pass
```

### Solution 3
```python
print(wlan.ifconfig())   # (ip, mask, gw, dns)
```

### Solution 4
```python
import urequests
resp = urequests.get("https://httpbin.org/get")
print(resp.status_code)
print(resp.json())
```

### Solution 5
```python
resp.close()
```

### Solution 6
```python
resp = urequests.post("https://httpbin.org/post",
                      json={"temp": 22.5})
resp.close()
```

### Solution 7
```python
try:
    wlan.connect("SSID", "password")
    if not wlan.isconnected():
        raise OSError("no network")
except OSError as e:
    print("failed:", e)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is WLAN?
- Wireless interface
- A pin
- A sensor
- None
* Correct answer: Wireless interface
network.

What is STA_IF?
- Station mode
- AP
- Both
- None
* Correct answer: Station mode
Client.

What is active(True)?
- Enables
- Disables
- Reads
- None
* Correct answer: Enables
Interface.

What is connect()?
- Joins network
- Disconnects
- Scans
- None
* Correct answer: Joins network
SSID.

What is isconnected?
- Status check
- Connects
- Disconnects
- None
* Correct answer: Status check
Boolean.

What is ifconfig?
- Network config
- Status
- Scan
- None
* Correct answer: Network config
IP.

What is urequests?
- HTTP client
- Sensor
- Wi-Fi
- None
* Correct answer: HTTP client
Micro.

What is get?
- Fetch
- Send
- Delete
- None
* Correct answer: Fetch
Request.

What is close?
- Frees connection
- Opens
- Reads
- None
* Correct answer: Frees connection
Important.

What is post?
- Submit
- Fetch
- Delete
- None
* Correct answer: Submit
Data.

What is status_code?
- Response code
- IP
- SSID
- None
* Correct answer: Response code
200.

What is a gateway?
- Network exit
- Device IP
- DNS
- None
* Correct answer: Network exit
ifconfig.
<!--/QUIZ-->
