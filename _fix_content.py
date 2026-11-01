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


def patch_lit(rel, old, new):
    path = ROOT / rel
    text = path.read_text(encoding='utf-8')
    if old not in text:
        print('НЕ НАЙДЕНО (literal):', rel)
        return False
    path.write_text(text.replace(old, new), encoding='utf-8')
    print('OK:', rel)
    return True


# 3) Flask: опечатка в execute
patch_lit('07-projects/02-project-todo-flask.md',
          'VALUES (?)\\ (title,))', 'VALUES (?)", (title,))')

# 4) Пайплайн: continue вне цикла -> комментарий
patch_lit('17-scraping/06-extraction-pipeline.md',
          'if not name:\n    continue                     # пропускаем пустые значения',
          'if not name:\n    # continue — внутри цикла пропускает пустые значения')

# 5) Книжная БД: фрагменты класса -> обёртка-заглушка
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
         r'```python\ndef to_dict\(self\):\n.*?\n```', book2_canon)

book4_canon = '''```python
import json


class Library:
    def __init__(self):
        self.books = []

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in self.books], f,
                      ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path):
        lib = cls()
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                lib.add_book(Book.from_dict(item))
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return lib
```
'''
patch_re('20-works/03-work-book-db.md',
         r'```python\nimport json\n\n    def save.*?\n```', book4_canon)

# 6) Сериализаторы: фрагмент -> функция
patch_re('22-drf/02-serializers.md',
         r'```python\nserializer = BookSerializer.*?\n```',
         '''```python
def book_list(request):
    serializer = BookSerializer(Book.objects.all(), many=True)
    return Response(serializer.data)
```
''')

# 7) Сериализация: bytes-литералы с кириллицей -> encode()
patch_lit('24-security/04-serialization-safety.md',
          'KEY = b"очень-секретный-ключ"', 'KEY = "очень-секретный-ключ".encode()')
patch_lit('24-security/04-serialization-safety.md',
          'KEY = b"секретный-ключ"', 'KEY = "секретный-ключ".encode()')

# 8) Криптография
patch_lit('24-security/05-cryptography.md',
          'password = b"Пароль123"', 'password = "Пароль123".encode()')
patch_lit('24-security/05-cryptography.md',
          'token = f.encrypt(b"секретные данные")',
          'token = f.encrypt("секретные данные".encode())')
patch_lit('24-security/05-cryptography.md',
          'key = b"ключ"', 'key = "ключ".encode()')

# 9) PyQt: фрагменты класса
patch_re('27-pyqt/08-app-project.md',
         r'```python\nimport sys, os\n.*?\n```',
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
         r'```python\ndef add_note\(self\):\n.*?\n```', app9_canon)

# 10) Любовь к Python: намеренно «не-Python» пример -> python-error
patch_re('30-love/01-why-python.md',
         r'```python\nprint\("Привет, мир!\)\n.*?\n```',
         '```python-error\nprint("Привет, мир!)\nprint("Меня зовут" Аня)\nпечать("Это не Python")\n```')
