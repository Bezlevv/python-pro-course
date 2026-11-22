---
title: Exam: Web Development
summary: Test your web development knowledge: HTTP, requests, HTML/CSS, Flask, Jinja2, FastAPI, Django, Streamlit, SQL, and JWT.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
What is the HTTP GET method for?
- To send data to the server
- To retrieve data from the server
- To update a resource
- To delete a resource
* Correct answer: To retrieve data from the server
GET requests a resource (a page, JSON, an image) without changing the server's state.

What does the HTTP status 404 mean?
- The server is working
- Resource not found
- Authorization is required
- Internal server error
* Correct answer: Resource not found
404 means the requested address does not exist on the server.

How do you get the response code of requests.get("https://example.com")?
- response.code
- response.status_code
- response.status
- response.http_code
* Correct answer: response.status_code
The Response object has a status_code attribute holding the HTTP status.

How do you bind a function to the "/" address in Flask?
- @app.route("/") above the function
- app.url("/", func)
- @route("/") above the function
- app.add_url("/")
* Correct answer: @app.route("/") above the function
The @app.route("/") decorator registers the function as the handler for the main page.

How do you output the value of the variable name in a Jinja2 template?
- <% name %>
- {{ name }}
- ${name}
- [[ name ]]
* Correct answer: {{ name }}
Double curly braces substitute the variable's value into the HTML.

Where does FastAPI show automatic interactive documentation?
- /docs
- /api
- /swagger.json
- /help
* Correct answer: /docs
FastAPI generates a Swagger UI at /docs — there you can run requests right in the browser.

What does the Django ORM do?
- Writes CSS styles
- Lets you work with the database through model classes instead of SQL
- Renders HTML templates
- Configures the web server
* Correct answer: Lets you work with the database through model classes instead of SQL
The ORM translates model calls into SQL queries, for example User.objects.filter(age=25).

Which call outputs text in Streamlit?
- sl.print("Hello!")
- st.write("Hello!")
- stream.write("Hello!")
- st.show("Hello!")
* Correct answer: st.write("Hello!")
st.write universally outputs text, numbers, DataFrames, and charts into a Streamlit app.

Which SQL query returns all records from the users table?
- SELECT * FROM users
- GET ALL FROM users
- FETCH * FROM users
- SHOW * FROM users
* Correct answer: SELECT * FROM users
SELECT selects data, and the asterisk means all columns.

What is JWT?
- A page markup language
- A token format for authentication
- A database
- A testing framework
* Correct answer: A token format for authentication
JWT (JSON Web Token) is a compact signed token that confirms the user's identity.
<!--/QUIZ-->
