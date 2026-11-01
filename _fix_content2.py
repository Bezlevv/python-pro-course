import re
from pathlib import Path

ROOT = Path(r'D:\AutoClaw\Python_PRO\content')


def patch_re(rel, pattern, repl, flags=re.S):
    path = ROOT / rel
    text = path.read_text(encoding='utf-8')
    new, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n == 0:
        print('НЕ НАЙДЕНО (regex):', rel)
        return False
    path.write_text(new, encoding='utf-8')
    print('OK:', rel)
    return True


book2_canon = '''```python
class Book:
    def __init__(self, title, author, year=2000, genre="", read=False, rating=None):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.read = read
        self.rating = rating

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
            "read": self.read,
            "rating": self.rating,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(title=data["title"], author=data["author"], year=data["year"],
                   genre=data["genre"], read=data["read"], rating=data["rating"])

    def __eq__(self, other):
        return (self.title == other.title and self.author == other.author)
```
'''
patch_re('20-works/03-work-book-db.md',
         r'```python\n    def to_dict\(self\):\n.*?\n```', book2_canon)

patch_re('27-pyqt/08-app-project.md',
         r'   ```python\n   import sys, os\n   def resource_path.*?\n   ```',
         '''```python
import sys
import os


def resource_path(relative):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)
```
''')

app9_canon = '''```python
class NotesWindow(QMainWindow):
    def __init__(self):
        self.notes = []
        self.edit = None
        self.list_widget = None

    def add_note(self):
        text = self.edit.text().strip()
        if not text:
            return
        self.notes.append(text)
        self.list_widget.addItem(text)
        self.edit.clear()

    def delete_note(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        answer = QMessageBox.question(
            self, "Удаление", "Удалить заметку?"
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.notes.pop(row)
            self.list_widget.takeItem(row)
```
'''
patch_re('27-pyqt/08-app-project.md',
         r'```python\n    def add_note\(self\):\n.*?\n```', app9_canon)
