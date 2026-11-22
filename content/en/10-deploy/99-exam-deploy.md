---
title: Exam: Deployment and Production
summary: Test your knowledge of Docker, GitHub Actions, Gunicorn and Nginx, hosting, environment variables and secrets.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
How does a Docker image differ from a container?
- They are synonyms
- An image is an immutable template, a container is a running instance of the image
- A container is a template, and an image is a running process
- An image exists only in Docker Hub
* Correct answer: An image is an immutable template, a container is a running instance of the image
Many containers can be run from one image; a container is a running process with its own environment.

Which Dockerfile instruction sets the default command when running a container?
- RUN
- EXPOSE
- CMD
- COPY
* Correct answer: CMD
CMD defines the default command. RUN executes commands at build time, and EXPOSE only declares a port.

Why does docker-compose.yml need a pgdata volume?
- To speed up the image build
- So database data survives container restarts and recreations
- To hide passwords from the config
- To limit network access
* Correct answer: So database data survives container restarts and recreations
A volume stores data outside the container's filesystem — it does not disappear when the container is recreated.

Which folder should GitHub Actions workflow files be placed in?
- In the root of the repository
- In the .github/workflows/ folder
- In the scripts/ folder
- In the config/ folder
* Correct answer: In the .github/workflows/ folder
GitHub looks for workflows specifically in .github/workflows/ — files from other folders are ignored.

What does the on block define in a GitHub Actions workflow?
- The type of machine used for execution
- Events (push, pull_request, and others) that trigger the workflow
- The list of secrets
- The name of the workflow
* Correct answer: Events (push, pull_request, and others) that trigger the workflow
The on block lists the triggers on which GitHub runs the pipeline.

What does needs: test guarantee in the docker job?
- The docker job will run before the tests
- The docker job will start only after the test job succeeds
- The docker job will have access to secrets
- The test job will run on the same machine as docker
* Correct answer: The docker job will start only after the test job succeeds
needs sets dependencies between jobs: the image will be published only when tests pass (green).

Why is the built-in Flask server unsuitable for production?
- It violates Python's license
- It is not designed for high loads and is meant for development
- It cannot handle HTTP
- It only works on Windows
* Correct answer: It is not designed for high loads and is meant for development
The built-in server was created for development convenience; in production the app is run through a separate WSGI server such as Gunicorn.

What does the -w 4 flag do in the gunicorn command?
- Sets the request timeout
- Starts four worker processes
- Enables debug mode
- Specifies the number of queued connections
* Correct answer: Starts four worker processes
Workers handle requests in parallel, which increases the application's throughput.

Why put Nginx in front of Gunicorn?
- To replace Gunicorn
- To serve static files, terminate SSL/TLS, balance load, and pass client headers
- To store the database
- To automatically restart the app
* Correct answer: To serve static files, terminate SSL/TLS, balance load, and pass client headers
Nginx serves static files directly from disk and proxies dynamic requests to Gunicorn — Python is not loaded with extra work.

Why must the .env file not be committed to git?
- Because it is too large
- Because it contains secrets: passwords, keys, tokens
- Because git does not support this format
- Because it interferes with the image build
* Correct answer: Because it contains secrets: passwords, keys, tokens
Publishing .env exposes secrets. Only the .env.example template with empty values is committed to git.
<!--/QUIZ-->
