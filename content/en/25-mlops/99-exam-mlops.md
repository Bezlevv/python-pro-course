---
title: Exam: MLOps
summary: Final knowledge check for the module "MLOps: from model to production".
order: 99
duration: 30 min
difficulty: advanced
exam: true
---

<!--QUIZ-->
What is a run in MLflow?
- A single experiment run with logging of parameters, metrics and artifacts
- A folder with training data
- A version of Python
* Correct answer: A single experiment run with logging of parameters, metrics and artifacts
A run is a separate training or inference run into which MLflow records everything related to that run: parameters, metrics, artifacts, the model.

How do parameters (params) differ from metrics (metrics) in MLflow?
- Parameters are model settings, metrics are the result of its work on data
- Parameters are floating-point numbers, metrics are integers
- They do not differ
* Correct answer: Parameters are model settings, metrics are the result of its work on data
Parameters (max_depth, learning_rate) are set before training, while metrics (accuracy, r2) are computed from the results and are needed to compare runs.

Why is the ONNX format needed?
- For a portable model representation that can be executed without the original framework
- For storing training data
- For deploying web servers
* Correct answer: For a portable model representation that can be executed without the original framework
ONNX describes a model as a computation graph; onnxruntime executes that graph quickly and without installing sklearn, PyTorch, etc.

What data type does a model input expect in onnxruntime by default?
- float32 (np.float32)
- float64
- int64
* Correct answer: float32 (np.float32)
ONNX models almost always work with float32 — it is the format standard. Passing float64 often causes an error, so the input must be converted with .astype(np.float32).

What will FastAPI with a Pydantic model return if a client sends invalid data (e.g., age = 15 with the constraint ge=18)?
- HTTP 422 Unprocessable Entity with an error description
- HTTP 200 and a prediction
- The server crashes with an exception
* Correct answer: HTTP 422 Unprocessable Entity with an error description
Pydantic automatically validates the request body. If the data fails the constraints, FastAPI returns 422 with details — without a single line of your code.

What is data drift?
- A change in the distribution of the model's input data after it is deployed
- An error in the service code
- An increase in response latency
* Correct answer: A change in the distribution of the model's input data after it is deployed
Data in the real world changes: users, seasons, the market. A model trained on an old distribution starts to perform worse — drift captures that.

Which PSI threshold indicates strong drift?
- PSI > 0.25
- PSI > 0.01
- PSI > 1.0
* Correct answer: PSI > 0.25
The classic scale: PSI < 0.1 — practically no drift, 0.1–0.25 — moderate, > 0.25 — strong drift, the model should be checked.

What does a DAG describe in Airflow?
- The order and dependencies of pipeline task execution (a directed acyclic graph)
- A neural network graph
- A database schema
* Correct answer: The order and dependencies of pipeline task execution (a directed acyclic graph)
Each task is a DAG node, and arrows show what must run before what. A DAG has no cycles: a pipeline always finishes.

Why is Airflow usually "heavier" than Prefect?
- Airflow requires separately running scheduler and webserver, while Prefect is just code with decorators
- Airflow is written in C++
- Prefect cannot run tasks
* Correct answer: Airflow requires separately running scheduler and webserver, while Prefect is just code with decorators
Airflow needs an infrastructure "skeleton" (scheduler + webserver + database); Prefect runs from an ordinary script and is easier to embed in a project.

What does p-value < 0.05 mean in an A/B test?
- The difference between the groups is statistically significant at the level α = 0.05
- The model is overfit
- The sample is too small
* Correct answer: The difference between the groups is statistically significant at the level α = 0.05
The p-value is the probability of seeing such a difference by chance if there is actually no difference. If p < α, we reject the null hypothesis and consider the effect significant.

What is point-in-time in a feature store?
- A feature value is returned strictly as of the request moment, not from the future — this protects against data leakage
- Storing features only in memory
- Disabling features during training
* Correct answer: A feature value is returned strictly as of the request moment, not from the future — this protects against data leakage
Point-in-time correctness means that during training and inference a feature is taken as of that moment in time: no information from the future — otherwise metrics would be inflated.
<!--/QUIZ-->
