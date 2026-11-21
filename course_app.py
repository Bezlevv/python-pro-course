"""Обёртка: открывает офлайн-курс в окне (pywebview) или системном браузере."""

import sys
from pathlib import Path


def find_html():
    # 1) рядом с exe (после сборки)
    base = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
    cand = base / 'PythonPro-Course.html'
    if cand.exists():
        return cand
    # 2) рядом со скриптом (режим разработки)
    cand = Path(__file__).resolve().parent / 'PythonPro-Course.html'
    if cand.exists():
        return cand
    return None


def main():
    html = find_html()
    if html is None:
        print('PythonPro-Course.html не найден рядом с приложением.')
        input('Нажми Enter для выхода...')
        return
    url = 'file:///' + str(html).replace('\\', '/')
    try:
        import webview  # type: ignore
        webview.create_window('PythonПро — офлайн-курс', url)
        webview.start()
    except Exception:
        import webbrowser
        webbrowser.open(str(html))


if __name__ == '__main__':
    main()
