---
title: Pagination, filtering, search
summary: Page numbers, filter backends.
order: 4
duration: 45 min
difficulty: advanced
tags: drf, pagination
---

Lists need paging and search.

## Pagination

```python
from rest_framework.pagination import PageNumberPagination

class BookPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
```

## Filtering

```python
from django_filters.rest_framework import DjangoFilterBackend

class BookViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "in_stock"]
```

## Search

```python
from rest_framework.filters import SearchFilter

class BookViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ["title", "author"]
```

## Lesson summary

Backends add ?page=, ?category=, ?search=.

<!--TASK-->
### Task 1 — Pagination
Add pagination with page_size 10.

### Task 2 — Request
Use ?page=2.

### Task 3 — Filter
Filter by category.

### Task 4 — Search
Search by title.

### Task 5 — Combine
Combine backends.

### Task 6 — Ordering
Add OrderingFilter.

### Task 7 — Response
Describe the paginated JSON.
<!--/TASK-->

<!--HINT-->
### Hint 1
PageNumberPagination.

### Hint 2
?page=.

### Hint 3
DjangoFilterBackend.

### Hint 4
SearchFilter.

### Hint 5
List.

### Hint 6
OrderingFilter.

### Hint 7
Count.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from rest_framework.pagination import PageNumberPagination

class BookPagination(PageNumberPagination):
    page_size = 10
```

### Solution 2
```text
GET /books/?page=2
```

### Solution 3
```python
from django_filters.rest_framework import DjangoFilterBackend

filter_backends = [DjangoFilterBackend]
filterset_fields = ["category"]
```

### Solution 4
```python
from rest_framework.filters import SearchFilter

filter_backends = [SearchFilter]
search_fields = ["title"]
```

### Solution 5
```python
filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
```

### Solution 6
```python
from rest_framework.filters import OrderingFilter

filter_backends = [OrderingFilter]
ordering_fields = ["price", "title"]
```

### Solution 7
```json
{"count": 45, "next": "...?page=2",
 "previous": null, "results": [...]}
```
<!--/SOLUTION-->

<!--QUIZ-->
What is pagination?
- Splitting pages
- All rows
- Sorting
- None
* Correct answer: Splitting pages
page_size.

What is PageNumberPagination?
- Page numbers
- Cursor
- None
- Search
* Correct answer: Page numbers
Class.

What is page_size?
- Rows per page
- Total
- Offset
- None
* Correct answer: Rows per page
20.

What is a filter?
- Condition
- Sort
- Page
- None
* Correct answer: Condition
category.

What is DjangoFilterBackend?
- ?field=value
- Search
- Order
- None
* Correct answer: ?field=value
Backend.

What is SearchFilter?
- ?search=text
- Filter
- Order
- None
* Correct answer: ?search=text
Lookup.

What is OrderingFilter?
- ?ordering=price
- Filter
- Search
- None
* Correct answer: ?ordering=price
Sort.

What is search_fields?
- Which fields
- Values
- Pages
- None
* Correct answer: Which fields
Title.

What is count?
- Total items
- Page
- Filter
- None
* Correct answer: Total items
JSON.

What is next?
- Next page URL
- Previous
- Results
- None
* Correct answer: Next page URL
Link.

What is results?
- Page items
- Count
- Next
- None
* Correct answer: Page items
Array.

What is the benefit?
- Fewer payloads
- Slower
- Required
- None
* Correct answer: Fewer payloads
Performance.
<!--/QUIZ-->
