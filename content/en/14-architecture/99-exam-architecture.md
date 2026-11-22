---
title: Exam: System Architecture
summary: Test your knowledge of SOLID, clean architecture, REST and GraphQL, microservices, message queues, caching, and idempotency.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
Which SOLID principle requires a class to have one reason to change?
- SRP
- OCP
- LSP
- DIP
* Correct answer: SRP
Single Responsibility — a class has one responsibility and one reason to change.

What does "open for extension, closed for modification" mean?
- New behavior is added with new code, not by editing existing code
- A class cannot be inherited
- All methods must be public
- Changes are forbidden
* Correct answer: New behavior is added with new code, not by editing existing code
This is the OCP principle: polymorphism instead of if/elif chains.

Where are dependencies directed in Clean Architecture?
- From outer layers inward
- From inner layers outward
- Inner layers depend on the database
- There are no dependencies
* Correct answer: From outer layers inward
The domain knows nothing about frameworks and databases; outer layers depend on domain abstractions.

What is a port in Clean Architecture?
- A network port
- An abstraction (protocol) that adapters implement
- A configuration file
- A FastAPI controller
* Correct answer: An abstraction (protocol) that adapters implement
A port describes the domain's need; an adapter is the implementation with a specific technology.

Which status code fits deleting a resource without a response body?
- 200
- 201
- 204
- 400
* Correct answer: 204
204 No Content — successful deletion without a response body.

What is GraphQL's main advantage over REST?
- The client itself selects the needed fields in one query
- No schema
- Works only with XML
- No server is required
* Correct answer: The client itself selects the needed fields in one query
A schema and one endpoint; the client requests exactly the fields it needs.

What is the main problem of microservices compared to a monolith?
- ACID transactions don't work across services
- Services can't be deployed
- There are no shared libraries
- They have no databases
* Correct answer: ACID transactions don't work across services
Sagas and compensations are needed, as well as control over network failures.

What does the strangler fig pattern do?
- Gradually replaces parts of a monolith with microservices through a facade
- Deletes all services
- Turns off logging
- Doubles the load
* Correct answer: Gradually replaces parts of a monolith with microservices through a facade
The facade hides the transition from the client; migration proceeds step by step.

Which message delivery mode requires an idempotent handler?
- At-most-once
- At-least-once
- Exactly-once
- None
* Correct answer: At-least-once
A message may arrive several times, and repeated processing must be harmless.

What is an idempotency key?
- A unique request identifier by which the server returns the stored result on a repeat
- A user password
- An encryption key
- A database index
* Correct answer: A unique request identifier by which the server returns the stored result on a repeat
This protects against double payments and other duplicates.
<!--/QUIZ-->
