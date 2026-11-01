import json
import re
import sys
from pathlib import Path

sys.path.insert(0, r'D:\AutoClaw\Python_PRO')

CONTENT = Path(r'D:\AutoClaw\Python_PRO\content')
FENCE_RE = re.compile(r'```python\s*\n(.*?)```', re.S)

FILES = [
    '01-basics/01-python-intro.md',
    '05-web/12-jwt-security.md',
    '07-projects/02-project-todo-flask.md',
    '17-scraping/06-extraction-pipeline.md',
    '20-works/03-work-book-db.md',
    '22-drf/02-serializers.md',
    '24-security/04-serialization-safety.md',
    '24-security/05-cryptography.md',
    '27-pyqt/08-app-project.md',
    '30-love/01-why-python.md',
]

for rel in FILES:
    path = CONTENT / rel
    text = path.read_text(encoding='utf-8')
    for idx, block in enumerate(FENCE_RE.findall(text), start=1):
        code = block.strip()
        if not code or any(h in code for h in ('…', '...', '>>> ', '<...>')):
            continue
        try:
            compile(code, str(path), 'exec')
        except SyntaxError as exc:
            print(rel, '| блок', idx, '| строка', exc.lineno, '|', exc.msg)
            print(json.dumps(code, ensure_ascii=False))
            print('---')
