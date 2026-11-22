---
title: Exam: Python Application Security
summary: Check how well you've learned the whole module: OWASP, secrets, web attacks, serialization, cryptography, and hardening.
order: 99
duration: 30 min
difficulty: advanced
exam: true
---

<!--QUIZ-->
What is OWASP Top 10?
- A list of the ten most common classes of web application risks
- Ten mandatory Python libraries
- Top-10 languages for web development
* Correct answer: A list of the ten most common classes of web application risks
OWASP Top 10 — risk categories from real attack data.

Which risk class describes IDOR — accessing foreign objects through a substituted id?
- A01 — Broken Access Control
- A03 — Injection
- A10 — SSRF
* Correct answer: A01 — Broken Access Control
Rights must be determined by verified user data, not by an id from the request.

How to read a secret from the environment correctly?
- os.environ.get(name) with a None check and an error
- Store the value right in code
- Write it to requirements.txt
* Correct answer: os.environ.get(name) with a None check and an error
Secrets come from the environment; a missing secret is a reason to fail.

Which tool checks dependencies for known CVEs?
- pip-audit
- git commit
- black
* Correct answer: pip-audit
pip-audit compares packages against the OSV database; safety is a similar tool.

What is SSRF?
- The server, at the attacker's bidding, accesses internal addresses
- Session cookie theft
- Buffer overflow
* Correct answer: The server, at the attacker's bidding, accesses internal addresses
Protection — blocking private, loopback, and link-local addresses.

Which string is an example of SQL injection?
- ' OR '1'='1
- SELECT * FROM users
- admin123
* Correct answer: ' OR '1'='1
Without parameterization it returns all table rows.

Why is pickle dangerous?
- It can execute arbitrary code on unpacking
- It is too slow
- It doesn't support dicts
* Correct answer: It can execute arbitrary code on unpacking
The __reduce__ method encodes a call to any function.

How does hashing differ from encryption?
- Hashing is one-way, encryption is reversible
- It's the same thing
- Encryption is slower
* Correct answer: Hashing is one-way, encryption is reversible
The original data cannot be recovered from a hash, but encrypted data can.

Why is salt needed when hashing passwords?
- So identical passwords give different hashes
- To speed up verification
- To shorten the hash
* Correct answer: So identical passwords give different hashes
Salt destroys rainbow hash tables.

What does RotatingFileHandler do?
- Truncates the log file when a size is reached and keeps backup copies
- Deletes all logs
- Encrypts logs
* Correct answer: Truncates the log file when a size is reached and keeps backup copies
maxBytes and backupCount limit the log volume.
<!--/QUIZ-->
