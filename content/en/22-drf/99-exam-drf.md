---
title: Exam: Django REST Framework
summary: Test yourself on the whole module: serializers, viewsets, JWT, filtering and testing.
order: 99
duration: 30 min
difficulty: advanced
exam: true
tags: drf, exam
---

<!--QUIZ-->
What does the Response class do in DRF?
- Forms a JSON response with correct headers
- Connects to the database
- Renders HTML pages
* Correct answer: Forms a JSON response with correct headers
Response turns an object into JSON and sets Content-Type and the status code.

Which method must be implemented in the base Serializer to create an object?
- create(validated_data)
- save_object()
- insert()
* Correct answer: create(validated_data)
The create method is called from save() when the object does not exist yet.

What does ModelSerializer do automatically?
- Generates fields, create() and update() from the model
- Creates the database
- Changes the table schema
* Correct answer: Generates fields, create() and update() from the model
ModelSerializer builds fields from the model and can save data.

Which class combines all CRUD into one class?
- ModelViewSet
- APIView
- ListAPIView
* Correct answer: ModelViewSet
ModelViewSet contains list, retrieve, create, update, partial_update, destroy.

What does DefaultRouter do?
- Automatically creates routes for ViewSet
- Generates migrations
- Checks passwords
* Correct answer: Automatically creates routes for ViewSet
Router.register("books", BookViewSet) builds all standard URLs.

How long does an access token live in SimpleJWT by default?
- 5 minutes
- 30 days
- 1 year
* Correct answer: 5 minutes
By default — 5 minutes, the lifetime changes via SIMPLE_JWT.

Which permission class allows access only to logged-in users?
- IsAuthenticated
- AllowAny
- IsAdminReadOnly
* Correct answer: IsAuthenticated
IsAuthenticated lets only authenticated users through.

Which parameter does SearchFilter use?
- ?search=...
- ?filter=...
- ?find=...
* Correct answer: ?search=...
SearchFilter searches for a substring in fields from search_fields.

What does the count key contain in a paginated response?
- Total number of records
- Page number
- Page size
* Correct answer: Total number of records
count is the number of records in the whole queryset, not on the page.

How to log in a client in APITestCase without a request?
- client.force_authenticate(user=user)
- client.login(user=user)
- client.auth(user=user)
* Correct answer: client.force_authenticate(user=user)
force_authenticate directly inserts the user into APIClient.
<!--/QUIZ-->
