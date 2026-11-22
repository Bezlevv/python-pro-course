---
title: Exam: Practical Projects
summary: Checking meta-skills: project planning, architecture, tests, deployment, independence.
order: 99
duration: 30 min
difficulty: advanced
tags: exam, projects
exam: true
---

<!--QUIZ-->
Where should you start writing any project?
- With writing code
- With formulating requirements and a plan
- With configuring the server
- With choosing the interface colors
* Correct answer: With formulating requirements and a plan
The plan and requirements define the scope, structure, and readiness criteria.

What is a "portfolio project"?
- A project you can show and explain at an interview
- Any educational project
- An open-source project
- A project that must be monetized
* Correct answer: A project you can show and explain at an interview
What matters isn't quantity but quality: readable code, tests, documentation, README.

Why does a project need automated tests?
- To write code faster
- To guarantee that changes don't break existing behavior
- To replace documentation
- To reduce the number of files
* Correct answer: To guarantee that changes don't break existing behavior
Tests are insurance during refactoring and project evolution.

Which tool is most often used to deploy a Python app in Docker?
- Gunicorn + Dockerfile
- Only python runserver
- Excel
- Jupyter Notebook
* Correct answer: Gunicorn + Dockerfile
Gunicorn is a production WSGI server; the Dockerfile describes the application image.

What is an "MVP"?
- A minimally viable product with the core functionality
- A maximally voluminous product
- A product for internal use
- Underdeveloped code
* Correct answer: A minimally viable product with the core functionality
An MVP lets you quickly test a hypothesis and get feedback.

Why does a project need a README.md file?
- To describe how to run and use the project
- It's only needed for GitHub
- To store secrets
- It's created automatically and isn't needed
* Correct answer: To describe how to run and use the project
README is the entry point for anyone opening the repository.

What does "refactoring" mean?
- Changing the internal structure of code without changing behavior
- Adding new features
- Fixing a bug
- Rewriting the project from scratch
* Correct answer: Changing the internal structure of code without changing behavior
Refactoring improves readability and maintainability without changing results.

How should secrets (API keys, passwords) be stored?
- In environment variables or a secret store
- In code next to the logic
- In README
- In variable names
* Correct answer: In environment variables or a secret store
Secrets must not get into git — this is a generally accepted security practice.

What is "code review"?
- Checking code by another developer before merging
- Automatic code formatting
- Running tests
- Describing code in comments
* Correct answer: Checking code by another developer before merging
Review catches errors and improves code quality.

Which criterion says a project is "ready"?
- The criteria from the requirements are met and the project passes checks
- The code compiles
- The author likes the project
- The project has more than 1000 lines
* Correct answer: The criteria from the requirements are met and the project passes checks
Readiness is defined by predetermined criteria: functionality, tests, documentation.
<!--/QUIZ-->
