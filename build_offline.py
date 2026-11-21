#!/usr/bin/env python
"""Собирает самодостаточный офлайн-HTML курса PythonПро."""

import os
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, r'D:\AutoClaw\Python_PRO')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courseproj.settings')

import django

django.setup()

from learn.models import Lesson, Module  # noqa: E402
from learn.utils import TASK_SECTION_RE, render_markdown, split_numbered_sections  # noqa: E402

OUT = Path(r'D:\AutoClaw\Python_PRO\PythonPro-Course.html')


def quiz_html(lesson):
    quizzes = list(lesson.quizzes.all())
    if not quizzes:
        return ''
    parts = [
        '<div class="quiz-block">',
        '<h3>✅ Викторина</h3>',
    ]
    for i, q in enumerate(quizzes):
        options = ''.join(
            f'<label class="quiz-option"><input type="radio" name="q{i}" '
            f'value="{j}"><span>{escape(opt)}</span></label>'
            for j, opt in enumerate(q.options)
        )
        parts.append(
            f'<div class="quiz-question" data-q="{i}" '
            f'data-correct="{q.correct_index}" '
            f'data-expl="{escape(q.explanation[:200])}">'
            f'<div class="quiz-text">{escape(q.question)}</div>'
            f'{options}<div class="quiz-feedback"></div></div>'
        )
    parts.append(
        '<button class="quiz-check" type="button" onclick="checkQuiz(this)">'
        'Проверить ответы</button>'
    )
    parts.append('<div class="quiz-score"></div>')
    parts.append('</div>')
    return '\n'.join(parts)


def build_lesson_html(lesson):
    out = [
        f'<h2>{escape(lesson.title)}</h2>',
        '<div class="meta"><span>' + escape(lesson.module.title) + '</span> · <span>'
        + escape(lesson.get_difficulty_display()) + '</span> · <span>'
        + escape(lesson.duration) + '</span></div>',
    ]
    if lesson.summary:
        out.append(f'<p class="summary">{escape(lesson.summary)}</p>')
    if lesson.theory_md:
        out.append('<div class="theory">' + render_markdown(lesson.theory_md) + '</div>')

    tasks = split_numbered_sections(lesson.task_md, TASK_SECTION_RE)
    if tasks:
        out.append('<div class="tasks"><h3>🎯 Задачи</h3>')
        hints = dict(split_numbered_sections(lesson.hint_md, TASK_SECTION_RE))
        solutions = dict(split_numbered_sections(lesson.solution_md, TASK_SECTION_RE))
        for num, body in tasks:
            out.append(f'<div class="task"><h4>Задача {num}</h4>')
            out.append(f'<div>{render_markdown(body)}</div>')
            if hints.get(num):
                out.append(
                    '<details class="hint"><summary>💡 Подсказка</summary><div>'
                    + render_markdown(hints[num]) + '</div></details>'
                )
            if solutions.get(num):
                out.append(
                    '<details class="solution"><summary>🔓 Разбор</summary><div>'
                    + render_markdown(solutions[num]) + '</div></details>'
                )
            out.append('</div>')
        out.append('</div>')

    out.append(quiz_html(lesson))
    return '\n'.join(out)


def build_sidebar(modules):
    rows = [
        '<div class="search-wrap"><input id="searchInput" placeholder="Поиск по курсу…" '
        'oninput="filterTree(this.value)"></div>',
        '<div id="tree">',
    ]
    for module in modules:
        lessons = list(module.lessons.all().order_by('order'))
        rows.append(
            f'<div class="module-block"><div class="module-title" onclick="toggleModule(this)">'
            f'{escape(module.icon)} {escape(module.title)} '
            f'<span class="cnt">{len(lessons)}</span></div>'
        )
        rows.append('<div class="lesson-list">')
        for lesson in lessons:
            rows.append(
                f'<div class="lesson-link" data-path="{lesson.id}" '
                f'onclick="openLesson({lesson.id})">{escape(lesson.title)}</div>'
            )
        rows.append('</div></div>')
    rows.append('</div>')
    return '\n'.join(rows)


def main():
    modules = list(Module.objects.all().order_by('order'))
    lessons = {l.id: l for l in Lesson.objects.select_related('module').all()}
    lessons_html = {lid: build_lesson_html(l) for lid, l in lessons.items()}
    sidebar = build_sidebar(modules)

    page = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PythonПро — офлайн-курс</title>
<style>
:root {{
  --bg:#0b0f17; --surface:#121826; --surface2:#171f30; --border:#22304a;
  --text:#e9edf6; --muted:#93a1bd; --accent:#7c5cff; --accent2:#22d3ee;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Inter,"Segoe UI",system-ui,sans-serif; background:var(--bg); color:var(--text); }}
#layout {{ display:flex; height:100vh; }}
#sidebar {{ width:340px; min-width:340px; background:var(--surface); border-right:1px solid var(--border); overflow-y:auto; padding:12px; }}
#content {{ flex:1; overflow-y:auto; padding:28px 36px; }}
.brand {{ font-size:20px; font-weight:800; margin-bottom:12px; }}
.brand span {{ background:linear-gradient(90deg,var(--accent),var(--accent2)); -webkit-background-clip:text; background-clip:text; color:transparent; }}
#searchInput {{ width:100%; padding:10px 12px; border-radius:10px; border:1px solid var(--border); background:var(--surface2); color:var(--text); font:inherit; margin-bottom:12px; }}
.module-block {{ margin-bottom:8px; }}
.module-title {{ cursor:pointer; padding:8px 10px; font-weight:700; border-radius:8px; }}
.module-title:hover {{ background:var(--surface2); }}
.cnt {{ color:var(--muted); font-size:12px; }}
.lesson-list {{ display:none; padding-left:14px; }}
.module-block.open .lesson-list {{ display:block; }}
.lesson-link {{ padding:6px 8px; border-radius:6px; cursor:pointer; color:var(--muted); font-size:14px; }}
.lesson-link:hover {{ background:var(--surface2); color:var(--text); }}
.lesson-link.active {{ background:rgba(124,92,255,.2); color:var(--text); }}
#content h2 {{ margin-top:0; }}
.meta {{ color:var(--muted); margin-bottom:12px; }}
.summary {{ color:var(--muted); }}
.theory {{ margin-bottom:20px; line-height:1.7; }}
.theory pre {{ background:#0a0e16; border:1px solid var(--border); padding:14px; border-radius:10px; overflow-x:auto; }}
.theory code {{ font-family:Consolas,monospace; }}
.theory table {{ border-collapse:collapse; }}
.theory th,.theory td {{ border:1px solid var(--border); padding:6px 10px; }}
.tasks .task {{ border:1px solid var(--border); border-radius:12px; padding:14px; margin-bottom:12px; background:var(--surface); }}
.hint,.solution {{ margin-top:8px; border:1px solid var(--border); border-radius:8px; padding:8px 10px; background:var(--surface2); }}
.quiz-block {{ border:1px solid var(--border); border-radius:12px; padding:16px; background:var(--surface); }}
.quiz-question {{ margin-bottom:12px; }}
.quiz-option {{ display:block; padding:6px 8px; border-radius:6px; cursor:pointer; }}
.quiz-option:hover {{ background:var(--surface2); }}
.quiz-check {{ margin-top:10px; padding:10px 18px; border:0; border-radius:10px; background:linear-gradient(90deg,var(--accent),var(--accent2)); color:#fff; font:inherit; font-weight:700; cursor:pointer; }}
.quiz-score {{ font-weight:700; margin-top:8px; color:var(--accent2); }}
.quiz-feedback {{ color:var(--muted); font-size:14px; min-height:18px; }}
.quiz-question.correct .quiz-text {{ color:#34d399; }}
.quiz-question.incorrect .quiz-text {{ color:#f87171; }}
</style>
</head>
<body>
<div id="layout">
  <div id="sidebar">
    <div class="brand">🐍 Python<span>Про</span></div>
    {sidebar}
  </div>
  <div id="content">
    <div id="home">
      <h1>PythonПро — офлайн-курс</h1>
      <p style="color:var(--muted)">39 модулей · {len(lessons)} уроков · всё работает без интернета.<br>
      Выбери модуль слева, чтобы начать.</p>
    </div>
    <div id="lessonView" style="display:none"></div>
  </div>
</div>
<script>
const lessons = {{js_lessons}};
function openLesson(id) {{
  const view = document.getElementById('lessonView');
  view.innerHTML = lessons[id] || '<p>Урок не найден</p>';
  view.style.display = 'block';
  document.getElementById('home').style.display = 'none';
  document.querySelectorAll('.lesson-link').forEach(el => {{
    el.classList.toggle('active', Number(el.dataset.path) === id);
  }});
  document.getElementById('content').scrollTop = 0;
}}
function toggleModule(el) {{
  el.parentElement.classList.toggle('open');
}}
function filterTree(q) {{
  q = q.trim().toLowerCase();
  document.querySelectorAll('.module-block').forEach(bl => {{
    let show = false;
    bl.querySelectorAll('.lesson-link').forEach(l => {{
      const match = !q || l.textContent.toLowerCase().includes(q);
      l.style.display = match ? '' : 'none';
      if (match) show = true;
    }});
    bl.style.display = show ? '' : 'none';
    if (q) bl.classList.add('open');
  }});
}}
function checkQuiz(btn) {{
  const block = btn.closest('.quiz-block');
  const questions = block.querySelectorAll('.quiz-question');
  let score = 0, total = questions.length;
  questions.forEach(q => {{
    const checked = q.querySelector('input:checked');
    const correct = Number(q.dataset.correct);
    const ok = checked && Number(checked.value) === correct;
    if (ok) score++;
    q.classList.toggle('correct', ok);
    q.classList.toggle('incorrect', !ok);
    const fb = q.querySelector('.quiz-feedback');
    const expl = q.dataset.expl || '';
    if (ok) fb.textContent = '✓ Верно! ' + expl;
    else {{
      fb.textContent = '✗ Неверно. ' + expl;
      const opts = q.querySelectorAll('input');
      if (opts[correct]) opts[correct].checked = true;
    }}
  }});
  block.querySelector('.quiz-score').textContent = 'Результат: ' + score + ' из ' + total;
}}
</script>
</body>
</html>
"""

    page = page.replace('{js_lessons}', repr(lessons_html))
    OUT.write_text(page, encoding='utf-8')
    print('OK:', OUT.name, '| размер:', round(OUT.stat().st_size / 1024 / 1024, 2), 'МБ')


if __name__ == '__main__':
    main()
