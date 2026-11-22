---
title: XPath and XML parsing
summary: lxml, XPath expressions.
order: 3
duration: 45 min
difficulty: intermediate
tags: xml, xpath
---

XML stores structured data; XPath queries it.

## XML

```xml
<library>
  <book>
    <title>Python</title>
    <author>Alice</author>
  </book>
  <book>
    <title>DevOps</title>
    <author>Bob</author>
  </book>
</library>
```

## lxml + XPath

```python
from lxml import etree
root = etree.fromstring(xml)
titles = root.xpath("//book/title/text()")
```

## Common paths

- //book — all books;
- //book/title — titles;
- //book[@id='1'] — attribute filter.

## Lesson summary

XPath selects nodes with compact expressions.

<!--TASK-->
### Task 1 — Parse
Parse XML with lxml.

### Task 2 — Titles
Get all titles.

### Task 3 — Filter
Get the book with id=1.

### Task 4 — Attribute
Read an attribute.

### Task 5 — Count
Count books.

### Task 6 — Iterate
Loop over books.

### Task 7 — Build
Build XML with etree.
<!--/TASK-->

<!--HINT-->
### Hint 1
etree.fromstring.

### Hint 2
//book/title.

### Hint 3
[@id].

### Hint 4
.get().

### Hint 5
count().

### Hint 6
Iter.

### Hint 7
SubElement.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from lxml import etree
root = etree.fromstring(xml)
```

### Solution 2
```python
titles = root.xpath("//book/title/text()")
print(titles)   # ['Python', 'DevOps']
```

### Solution 3
```python
book = root.xpath("//book[@id='1']")[0]
```

### Solution 4
```python
print(book.get("id"))
```

### Solution 5
```python
print(len(root.xpath("//book")))
```

### Solution 6
```python
for book in root.xpath("//book"):
    title = book.xpath("title/text()")[0]
    author = book.xpath("author/text()")[0]
    print(title, author)
```

### Solution 7
```python
root = etree.Element("library")
book = etree.SubElement(root, "book")
etree.SubElement(book, "title").text = "Python"
print(etree.tostring(root, pretty_print=True).decode())
```
<!--/SOLUTION-->

<!--QUIZ-->
What is XML?
- Structured markup
- HTML
- JSON
- None
* Correct answer: Structured markup
Tags.

What is XPath?
- Node query language
- A parser
- A format
- None
* Correct answer: Node query language
Path.

What is lxml?
- XML library
- HTTP
- Database
- None
* Correct answer: XML library
Fast.

What is //book?
- All books
- First
- Title
- None
* Correct answer: All books
Descendant.

What is text()?
- Node text
- Attribute
- Tag
- None
* Correct answer: Node text
Value.

What is [@id='1']?
- Attribute filter
- Text filter
- Tag
- None
* Correct answer: Attribute filter
Predicate.

What is get()?
- Reads attribute
- Sets
- Deletes
- None
* Correct answer: Reads attribute
Attrib.

What is SubElement?
- Creates child
- Finds
- Deletes
- None
* Correct answer: Creates child
Build.

What is tostring?
- Serializes
- Parses
- Finds
- None
* Correct answer: Serializes
Bytes.

What is a node?
- XML element
- Text only
- File
- None
* Correct answer: XML element
Element.

What is pretty_print?
- Indents output
- Compresses
- Removes
- None
* Correct answer: Indents output
Readable.

What is a root?
- Top element
- Child
- Attribute
- None
* Correct answer: Top element
Library.
<!--/QUIZ-->
