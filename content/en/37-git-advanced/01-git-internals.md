---
title: Git internals
summary: Objects, refs, the index.
order: 1
duration: 45 min
difficulty: advanced
tags: git
---

Git stores snapshots as objects.

## Objects

- Blob: file content;
- Tree: directory snapshot;
- Commit: metadata + tree + parent.

## Refs

Branches are pointers to commits.

## Commands

```bash
git cat-file -p HEAD
git log --oneline --graph
```

## Lesson summary

Commits → trees → blobs; branches point.

<!--TASK-->
### Task 1 — Objects
Name three object types.

### Task 2 — Blob
What is a blob?

### Task 3 — Tree
What is a tree?

### Task 4 — Commit
What does a commit hold?

### Task 5 — Refs
What is a branch?

### Task 6 — Hash
Why SHA-1?

### Task 7 — Explore
Inspect HEAD.
<!--/TASK-->

<!--HINT-->
### Hint 1
Blob.

### Hint 2
Content.

### Hint 3
Dir.

### Hint 4
Parent.

### Hint 5
Pointer.

### Hint 6
Integrity.

### Hint 7
cat-file.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
Blob, tree, commit (плюс tag)
```

### Solution 2
```text
Blob — содержимое файла (без имени)
```

### Solution 3
```text
Tree — снимок каталога: имена и ссылки на блобы
```

### Solution 4
```text
Дерево, родитель(и), автор, сообщение, время
```

### Solution 5
```text
Ветка — перемещаемый указатель на коммит
```

### Solution 6
```text
SHA-1 даёт целостность: изменение содержимого
меняет хеш — подмена заметна
```

### Solution 7
```bash
git cat-file -p HEAD
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a blob?
- File content
- Directory
- Commit
- None
* Correct answer: File content
Snapshot.

What is a tree?
- Directory snapshot
- File
- Pointer
- None
* Correct answer: Directory snapshot
Names.

What is a commit?
- Snapshot + meta
- File
- Branch
- None
* Correct answer: Snapshot + meta
Message.

What is a parent?
- Previous commit
- Next
- Tree
- None
* Correct answer: Previous commit
Chain.

What is a ref?
- Pointer
- Object
- File
- None
* Correct answer: Pointer
Branch.

What is HEAD?
- Current commit
- Branch
- Object
- None
* Correct answer: Current commit
Now.

What is SHA-1?
- Hash
- File
- Branch
- None
* Correct answer: Hash
Integrity.

What is immutable?
- Can't change
- Changes
- Deletes
- None
* Correct answer: Can't change
Object.

What is a hash?
- Unique id
- Content
- Message
- None
* Correct answer: Unique id
Checksum.

What is cat-file?
- Inspects object
- Creates
- Deletes
- None
* Correct answer: Inspects object
-p.

What is a graph?
- History shape
- File
- Object
- None
* Correct answer: History shape
Branches.

What is the .git dir?
- Metadata store
- Working files
- Remote
- None
* Correct answer: Metadata store
Objects.
<!--/QUIZ-->
