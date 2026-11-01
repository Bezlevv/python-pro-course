#!/usr/bin/env python
"""
Проверщик примеров кода в уроках курса.

Запуск:  python check_code_samples.py

Делает:
1. Собирает все ```python-блоки из теории и разборов всех уроков.
2. Проверяет их синтаксис (compile).
3. Для безопасных блоков (без импортов) пробует выполнить их
   в песочнице и сообщает о runtime-ошибках как о предупреждениях.

Блоки-заглушки (содержат '…', '...', '>>> ' или '<...>') пропускаются.
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courseproj.settings')

import django

django.setup()

from learn.utils import run_python_code

CONTENT = Path(__file__).resolve().parent / 'content'
FENCE_RE = re.compile(r'```(python|python-error)\s*\n(.*?)```', re.S)
SKIP_HINTS = ('…', '...', '>>> ', '<...>', 'PYTHONPATH', 'from __future__')
ENV_DEP_TOKENS = ('open(', 'breakpoint(', 'input(')


def looks_like_stub(code):
    return any(hint in code for hint in SKIP_HINTS)


def main():
    errors = []
    warnings = []
    total_blocks = 0
    checked = 0
    skipped = 0
    env_dep = 0

    for folder in sorted(CONTENT.iterdir()):
        if not folder.is_dir() or folder.name.startswith('.'):
            continue
        for path in sorted(folder.glob('*.md')):
            if path.name == 'module.md' or path.name.startswith('99-'):
                continue
            text = path.read_text(encoding='utf-8')
            matches = FENCE_RE.findall(text)
            for lang, block in matches:
                total_blocks += 1
                code = block.strip()
                if not code or lang == 'python-error' or looks_like_stub(code):
                    skipped += 1
                    continue
                checked += 1
                try:
                    compile(code, str(path), 'exec')
                except SyntaxError as exc:
                    errors.append(f'{path.name}: синтаксис ({exc.lineno}): {exc.msg}')
                    continue
                if any(tok in code for tok in ENV_DEP_TOKENS):
                    env_dep += 1
                    continue
                if 'import' not in code and len(code) < 500:
                    result = run_python_code(code)
                    if not result.get('ok') and result.get('error'):
                        warnings.append(f'{path.name}: runtime: {result["error"][:120]}')

    print(f'Блоков кода найдено: {total_blocks} (проверено {checked}, пропущено-заглушек {skipped}, средозависимых {env_dep})')
    if errors:
        print(f'\nОШИБКИ синтаксиса ({len(errors)}):')
        for e in errors:
            print('  - ' + e)
    if warnings:
        print(f'\nПредупреждения runtime ({len(warnings)}):')
        for w in warnings:
            print('  - ' + w)
    print('\nИтог: ' + ('ЕСТЬ ОШИБКИ' if errors else 'OK (без синтаксических ошибок)'))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
