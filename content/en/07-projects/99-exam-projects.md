---
title: Exam: Practical Projects
summary: Test your knowledge of six complete projects: a game, a ToDo app with Flask, an API with FastAPI, a blog with Django, a dashboard with Streamlit, and a neural network.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
Which function does the "Guess the Number" game use to pick a number from 1 to 100?
- random.randint(1, 100)
- random.choice(range(100))
- int(random.random() * 100)
- random.sample(1, 100)
* Correct answer: random.randint(1, 100)
random.randint(a, b) returns an integer from a to b inclusive.

What happens if the player enters "abc" and the program calls int(input(...))?
- The program keeps running and substitutes 0
- A ValueError exception is raised
- "abc" gets printed
- The program asks the player again
* Correct answer: A ValueError exception is raised
input() always returns a string, and int("abc") cannot convert it. That is why input is wrapped in try/except and the player is asked to repeat.

What stack is the ToDo manager built on?
- Flask + Jinja2 + SQLite
- Django + PostgreSQL
- FastAPI + MongoDB
- Streamlit + Pandas
* Correct answer: Flask + Jinja2 + SQLite
Flask is a web framework, Jinja2 handles templates, and SQLite is the built-in database for storing tasks.

Why does a FastAPI API need a Pydantic model?
- To draw the user interface
- To describe the data structure and automatically validate incoming data
- To store data in the database
- To speed up server responses
* Correct answer: To describe the data structure and automatically validate incoming data
Type annotations and Field(ge=..., le=...) set constraints; if data fails validation, FastAPI itself returns error 422.

What does the Post model describe in a Django blog?
- The site's user
- An article: title, text, date
- A comment on an article
- Blog settings
* Correct answer: An article: title, text, date
A model is a table in the database; after describing it, migrations are created, and articles can be managed through the admin panel.

Which Streamlit call displays a key metric (for example, total revenue)?
- st.metric("Revenue", value)
- st.text(value)
- st.write_metric(value)
- st.show(value)
* Correct answer: st.metric("Revenue", value)
st.metric shows a value with a label — the standard way to display a metric on a dashboard.

Why cache data loading in a Streamlit dashboard?
- So data isn't recomputed on every filter change
- To reduce the size of the data file
- To make charts colorful
- So widgets don't display
* Correct answer: So data isn't recomputed on every filter change
Streamlit reruns the script on every interaction; caching (st.cache_data) lets heavy operations run only once.

Which HTTP methods make up CRUD in a FastAPI API?
- GET, POST, PUT, DELETE
- OPEN, CLOSE, READ, WRITE
- SELECT, INSERT, UPDATE, DELETE
- GET, SET, PUSH, POP
* Correct answer: GET, POST, PUT, DELETE
CRUD is creating (POST), reading (GET), updating (PUT), and deleting (DELETE) a resource.

How do you save a trained PyTorch model to a file?
- torch.save(model.state_dict(), "model.pth")
- model.save("model.pth")
- pickle.dump(model, "model.pth")
- torch.export(model, "model.pth")
* Correct answer: torch.save(model.state_dict(), "model.pth")
state_dict holds the model's weights; when loading, you create a model with the same architecture and call load_state_dict().

Why create a virtual environment for a project?
- To speed up code execution
- To isolate the project's dependencies from the system and other projects
- So the code runs without Python
- To deploy the project automatically
* Correct answer: To isolate the project's dependencies from the system and other projects
A virtual environment stores its packages separately, so different projects don't conflict over library versions.
<!--/QUIZ-->
