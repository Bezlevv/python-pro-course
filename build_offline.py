#!/usr/bin/env python
"""Собирает продвинутый офлайн-HTML курса PythonПро.
Возможности: редактор с автодополнением (CodeMirror), Python-песочница (Pyodide),
прогресс/закладки (localStorage), тёмная/светлая тема, навигация prev/next.
"""

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
RES = 'offline_res/'


def quiz_html(lesson):
    quizzes = list(lesson.quizzes.all())
    if not quizzes:
        return ''
    parts = ['<div class="quiz-block">', '<h3>✅ Викторина</h3>']
    for i, q in enumerate(quizzes):
        options = ''.join(
            f'<label class="quiz-option"><input type="radio" name="q{i}" '
            f'value="{j}"><span>{escape(opt)}</span></label>'
            for j, opt in enumerate(q.options)
        )
        parts.append(
            f'<div class="quiz-question" data-q="{i}" data-correct="{q.correct_index}" '
            f'data-expl="{escape(q.explanation[:200])}">'
            f'<div class="quiz-text">{escape(q.question)}</div>{options}'
            f'<div class="quiz-feedback"></div></div>'
        )
    parts.append('<button class="quiz-check" type="button" onclick="checkQuiz(this)">Проверить ответы</button>')
    parts.append('<div class="quiz-score"></div></div>')
    return '\n'.join(parts)


def build_lesson_html(lesson):
    out = [
        '<div class="lesson-toolbar">',
        f'<button class="fav-btn" onclick="toggleFav({lesson.id})">★ Избранное</button>',
        f'<button class="done-btn" onclick="toggleDone({lesson.id})">✓ Пройдено</button>',
        '<div class="toolbar-nav">',
        '<button class="nav-btn" onclick="navLesson(-1)">← Предыдущий</button>',
        '<button class="nav-btn" onclick="navLesson(1)">Следующий →</button>',
        '</div></div>',
        '<textarea class="note-area" id="noteArea" placeholder="📝 Моя заметка к уроку (сохраняется автоматически)"></textarea>',
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
                out.append('<details class="hint"><summary>💡 Подсказка</summary><div>'
                           + render_markdown(hints[num]) + '</div></details>')
            if solutions.get(num):
                out.append('<details class="solution"><summary>🔓 Разбор</summary><div>'
                           + render_markdown(solutions[num]) + '</div></details>')
            out.append('</div>')
        out.append('</div>')

    out.append(
        '<div class="sandbox">'
        '<h3>⚡ Песочница Python</h3>'
        '<textarea id="codeEditor" placeholder="# Напиши код и нажми «Запустить»"></textarea>'
        '<div class="sb-actions">'
        '<button class="run-btn" onclick="runCode()">Запустить ▶</button>'
        '<button class="run-btn ghost" onclick="clearOutput()">Очистить</button>'
        '</div>'
        '<pre id="output"></pre>'
        '</div>'
    )
    out.append(quiz_html(lesson))
    return '\n'.join(out)


def build_sidebar(modules):
    rows = [
        '<div class="search-wrap"><input id="searchInput" placeholder="Поиск…" '
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


CSS = """
:root{--bg:#0b0f17;--surface:#121826;--surface2:#171f30;--border:#22304a;--text:#e9edf6;--muted:#93a1bd;--accent:#7c5cff;--accent2:#22d3ee;}
[data-theme="light"]{--bg:#f4f6fb;--surface:#fff;--surface2:#eef1f8;--border:#dbe2ef;--text:#161d2e;--muted:#5b6b88;}
*{box-sizing:border-box;}
body{margin:0;font-family:Inter,"Segoe UI",system-ui,sans-serif;background:var(--bg);color:var(--text);}
#layout{display:flex;height:100vh;}
#sidebar{width:340px;min-width:340px;background:var(--surface);border-right:1px solid var(--border);overflow-y:auto;padding:12px;}
#content{flex:1;overflow-y:auto;padding:28px 36px;}
.brand{font-size:20px;font-weight:800;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;}
.brand span{background:linear-gradient(90deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;color:transparent;}
#searchInput{width:100%;padding:10px 12px;border-radius:10px;border:1px solid var(--border);background:var(--surface2);color:var(--text);font:inherit;margin-bottom:12px;}
.module-block{margin-bottom:8px;}
.module-title{cursor:pointer;padding:8px 10px;font-weight:700;border-radius:8px;}
.module-title:hover{background:var(--surface2);}
.cnt{color:var(--muted);font-size:12px;}
.lesson-list{display:none;padding-left:14px;}
.module-block.open .lesson-list{display:block;}
.lesson-link{padding:6px 8px;border-radius:6px;cursor:pointer;color:var(--muted);font-size:14px;display:flex;gap:6px;}
.lesson-link.done{color:#34d399;}
.lesson-link:hover{background:var(--surface2);color:var(--text);}
.lesson-link.active{background:rgba(124,92,255,.2);color:var(--text);}
#content h2{margin-top:0;}
.meta{color:var(--muted);margin-bottom:12px;}
.lesson-toolbar{display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap;}
.fav-btn,.done-btn,.nav-btn,.run-btn{border:1px solid var(--border);background:var(--surface2);color:var(--text);padding:8px 14px;border-radius:10px;cursor:pointer;font:inherit;}
.fav-btn.active{background:rgba(251,191,36,.2);}
.done-btn.active{background:rgba(52,211,153,.2);}
.toolbar-nav{margin-left:auto;display:flex;gap:8px;}
.summary{color:var(--muted);}
.theory{margin-bottom:20px;line-height:1.7;}
.theory pre{background:#0a0e16;border:1px solid var(--border);padding:14px;border-radius:10px;overflow-x:auto;}
.theory code{font-family:Consolas,monospace;}
.theory table{border-collapse:collapse;}
.theory th,.theory td{border:1px solid var(--border);padding:6px 10px;}
.tasks .task{border:1px solid var(--border);border-radius:12px;padding:14px;margin-bottom:12px;background:var(--surface);}
.hint,.solution{margin-top:8px;border:1px solid var(--border);border-radius:8px;padding:8px 10px;background:var(--surface2);}
.sandbox{border:1px solid var(--border);border-radius:12px;padding:16px;margin:16px 0;background:var(--surface);}
.sandbox .CodeMirror{height:200px;border:1px solid var(--border);border-radius:8px;}
.sb-actions{display:flex;gap:10px;margin-top:10px;}
#output{background:#0a0e16;border:1px solid var(--border);min-height:60px;padding:12px;border-radius:8px;white-space:pre-wrap;}
.quiz-block{border:1px solid var(--border);border-radius:12px;padding:16px;background:var(--surface);}
.quiz-question{margin-bottom:12px;}
.quiz-option{display:block;padding:6px 8px;border-radius:6px;cursor:pointer;}
.quiz-option:hover{background:var(--surface2);}
.quiz-check{margin-top:10px;padding:10px 18px;border:0;border-radius:10px;background:linear-gradient(90deg,var(--accent),var(--accent2));color:#fff;font:inherit;font-weight:700;cursor:pointer;}
.quiz-score{font-weight:700;margin-top:8px;color:var(--accent2);}
.quiz-feedback{color:var(--muted);font-size:14px;min-height:18px;}
.quiz-question.correct .quiz-text{color:#34d399;}
.quiz-question.incorrect .quiz-text{color:#f87171;}
#progressLine{font-size:13px;color:var(--muted);margin-bottom:12px;}
.copy-btn{position:absolute;top:8px;right:8px;border:1px solid var(--border);background:var(--surface2);color:var(--muted);font-size:11px;padding:3px 10px;border-radius:6px;cursor:pointer;font-family:inherit;}
.theory pre{position:relative;}
.note-area{width:100%;min-height:64px;margin:10px 0;background:var(--surface2);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:10px;font:inherit;resize:vertical;}

"""

JS = """
const lessons = @@LESSONS@@;
const lessonIds = @@IDS@@;
let activeId = null;
let editor = null;
let pyodide = null;
let pyReady = null;

function applyTheme(){
  const t = localStorage.getItem('pp_theme') || 'dark';
  document.body.dataset.theme = t;
  const b = document.querySelector('.brand .nav-btn');
  if (b) b.textContent = t === 'light' ? '🌙' : '☀️';
}
function toggleTheme(){
  const t = document.body.dataset.theme === 'light' ? 'dark' : 'light';
  localStorage.setItem('pp_theme', t);
  applyTheme();
}

function doneIds(){ return JSON.parse(localStorage.getItem('pp_done') || '[]'); }
function saveDone(ids){ localStorage.setItem('pp_done', JSON.stringify(ids)); }
function favIds(){ return JSON.parse(localStorage.getItem('pp_fav') || '[]'); }
function saveFav(ids){ localStorage.setItem('pp_fav', JSON.stringify(ids)); }

function updateProgress(){
  const total = lessonIds.length;
  const done = doneIds().filter(id => lessonIds.includes(id)).length;
  const pct = total ? Math.round(done / total * 100) : 0;
  document.getElementById('progressLine').textContent = 'Прогресс: ' + pct + '% (' + done + '/' + total + ')';
}

function syncLessonUI(){
  const done = doneIds();
  const fav = favIds();
  document.querySelectorAll('.lesson-link').forEach(el => {
    const id = Number(el.dataset.path);
    el.classList.toggle('done', done.includes(id));
    el.classList.toggle('fav', fav.includes(id));
  });
  const view = document.getElementById('lessonView');
  if (!view || activeId == null) return;
  const doneBtn = view.querySelector('.done-btn');
  const favBtn = view.querySelector('.fav-btn');
  if (doneBtn) doneBtn.classList.toggle('active', done.includes(activeId));
  if (favBtn) favBtn.classList.toggle('active', fav.includes(activeId));
}

function toggleDone(id){
  let ids = doneIds();
  ids = ids.includes(id) ? ids.filter(x => x !== id) : [...ids, id];
  saveDone(ids);
  updateProgress(); syncLessonUI();
}
function toggleFav(id){
  let ids = favIds();
  ids = ids.includes(id) ? ids.filter(x => x !== id) : [...ids, id];
  saveFav(ids);
  syncLessonUI();
}

function openLesson(id){
  activeId = id;
  const view = document.getElementById('lessonView');
  view.innerHTML = lessons[id] || '<p>Урок не найден</p>';
  view.style.display = 'block';
  document.getElementById('home').style.display = 'none';
  document.querySelectorAll('.lesson-link').forEach(el => {
    el.classList.toggle('active', Number(el.dataset.path) === id);
  });
  localStorage.setItem('pp_last', String(id));
  document.getElementById('content').scrollTop = 0;
  initEditor();
  syncLessonUI();
}
function navLesson(dir){
  const idx = lessonIds.indexOf(activeId);
  if (idx === -1) return;
  const nid = lessonIds[idx + dir] ?? activeId;
  openLesson(nid);
}
function toggleModule(el){ el.parentElement.classList.toggle('open'); }

function filterTree(q){
  q = q.trim().toLowerCase();
  document.querySelectorAll('.module-block').forEach(bl => {
    let show = false;
    bl.querySelectorAll('.lesson-link').forEach(l => {
      const match = !q || l.textContent.toLowerCase().includes(q);
      l.style.display = match ? '' : 'none';
      if (match) show = true;
    });
    bl.style.display = show ? '' : 'none';
    if (q) bl.classList.add('open');
  });
}

const PY_WORDS = ['and','as','assert','async','await','break','class','continue','def','del','elif','else','except','finally','for','from','global','if','import','in','is','lambda','nonlocal','not','or','pass','raise','return','try','while','with','yield','True','False','None','print','len','range','int','float','str','list','dict','set','tuple','bool','input','sum','min','max','abs','sorted','enumerate','zip','map','filter','type','isinstance','open','Exception','ValueError','TypeError','KeyError','IndexError'];

function pythonHints(cm){
  const cur = cm.getCursor();
  const line = cm.getLine(cur.line);
  const m = line.slice(0, cur.ch).match(/[\w$]+$/);
  if (!m) return null;
  const prefix = m[0].toLowerCase();
  const localWords = new Set();
  cm.getValue().replace(/\b([A-Za-z_][\w]*)\b/g, (x) => localWords.add(x));
  const all = new Set([...localWords, ...PY_WORDS]);
  const list = [...all].filter(w => w.toLowerCase().startsWith(prefix)).sort().slice(0, 30);
  return { list: list.map(w => ({ text: w })), from: CodeMirror.Pos(cur.line, cur.ch - prefix.length), to: cur };
}

function initEditor(){
  const ta = document.getElementById('codeEditor');
  if (!ta){ editor = null; return; }
  if (editor){ editor.toTextArea(); editor = null; }
  editor = CodeMirror.fromTextArea(ta, {
    mode: 'python',
    lineNumbers: true,
    indentUnit: 4,
    extraKeys: {'Ctrl-Space': 'autocomplete'},
    hintOptions: { hint: pythonHints }
  });
  editor.on('inputRead', cm => {
    if (cm.state.completionActive) return;
    cm.showHint({ hint: pythonHints });
  });
}

async function ensurePyodide(){
  if (pyodide) return pyodide;
  if (!pyReady){
    pyReady = (async () => {
      try {
        pyodide = await loadPyodide({ indexURL: '@@RES@@' });
      } catch (e) {
        pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/' });
      }
      return pyodide;
    })();
  }
  return pyReady;
}

async function runCode(){
  const out = document.getElementById('output');
  if (!editor){ out.textContent = 'Редактор недоступен'; return; }
  out.textContent = 'Выполняется…';
  try {
    const py = await ensurePyodide();
    let result = '';
    py.setStdout({ batched: s => { result += s + '\n'; } });
    const r = await py.runPythonAsync(editor.getValue());
    if (r !== undefined) result += String(r);
    out.textContent = result || '✓ Программа завершилась без вывода.';
  } catch (e) {
    out.textContent = 'Ошибка: ' + (e.message || e);
  }
}
function clearOutput(){ document.getElementById('output').textContent = ''; }

function checkQuiz(btn){
  const block = btn.closest('.quiz-block');
  const questions = block.querySelectorAll('.quiz-question');
  let score = 0, total = questions.length;
  questions.forEach(q => {
    const checked = q.querySelector('input:checked');
    const correct = Number(q.dataset.correct);
    const ok = checked && Number(checked.value) === correct;
    if (ok) score++;
    q.classList.toggle('correct', ok);
    q.classList.toggle('incorrect', !ok);
    const fb = q.querySelector('.quiz-feedback');
    const expl = q.dataset.expl || '';
    if (ok) fb.textContent = '✓ Верно! ' + expl;
    else {
      fb.textContent = '✗ Неверно. ' + expl;
      const opts = q.querySelectorAll('input');
      if (opts[correct]) opts[correct].checked = true;
    }
  });
  block.querySelector('.quiz-score').textContent = 'Результат: ' + score + ' из ' + total;
}


function decoratePreBlocks(){
  document.querySelectorAll('.theory pre').forEach(pre => {
    if (pre.querySelector('.copy-btn')) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-btn';
    btn.textContent = 'Копировать';
    btn.onclick = () => {
      const code = pre.querySelector('code');
      const txt = code ? code.innerText : pre.innerText;
      navigator.clipboard.writeText(txt).then(() => {
        btn.textContent = '✓ Скопировано';
        setTimeout(() => btn.textContent = 'Копировать', 1500);
      });
    };
    pre.appendChild(btn);
  });
}

function notes() { return JSON.parse(localStorage.getItem('pp_notes') || '{}'); }
function initNotes(){
  const ta = document.getElementById('noteArea');
  if (!ta || activeId == null) return;
  ta.value = notes()[activeId] || '';
  ta.oninput = () => {
    const n = notes();
    n[activeId] = ta.value;
    localStorage.setItem('pp_notes', JSON.stringify(n));
  };
}

function exportProgress(){
  const data = {
    exported: new Date().toISOString(),
    done: doneIds(),
    fav: favIds(),
    notes: notes(),
    lastLesson: localStorage.getItem('pp_last') || null,
    theme: localStorage.getItem('pp_theme') || 'dark'
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'pythonpro-progress.json';
  a.click();
}

// в openLesson добавляем decoratePreBlocks + initNotes
const originalOpen = openLesson;
openLesson = function(id){
  originalOpen(id);
  decoratePreBlocks();
  initNotes();
};

applyTheme();
const last = localStorage.getItem('pp_last');
if (last && lessons[last]) openLesson(Number(last));
updateProgress();
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PythonПро — офлайн-курс</title>
<link rel="stylesheet" href="@@RES@@codemirror.min.css">
<link rel="stylesheet" href="@@RES@@show-hint.min.css">
<style>@@CSS@@</style>
</head>
<body data-theme="dark">
<div id="layout">
  <div id="sidebar">
    <div class="brand">🐍 Python<span>Про</span><button class="nav-btn" onclick="toggleTheme()" title="Тема">🌙</button><button class="nav-btn" onclick="exportProgress()" title="Экспорт прогресса">⬇</button></div>
    <div id="progressLine">Прогресс: 0%</div>
    @@SIDEBAR@@
  </div>
  <div id="content">
    <div id="home">
      <h1>PythonПро — офлайн-курс</h1>
      <p style="color:var(--muted)">39 модулей · @@COUNT@@ уроков.<br>
      Функции: Python-песочница, автодополнение кода, викторины, прогресс, закладки, тёмная/светлая тема.</p>
    </div>
    <div id="lessonView" style="display:none"></div>
  </div>
</div>
<script src="@@RES@@codemirror.min.js"></script>
<script src="@@RES@@python.min.js"></script>
<script src="@@RES@@show-hint.min.js"></script>
<script src="@@RES@@pyodide.js"></script>
<script>@@JS@@</script>
</body>
</html>
"""


def main():
    modules = list(Module.objects.all().order_by('order'))
    lessons = {l.id: l for l in Lesson.objects.select_related('module').all()}
    lessons_html = {lid: build_lesson_html(l) for lid, l in lessons.items()}
    lesson_ids = [l.id for l in Lesson.objects.select_related('module').order_by('module__order', 'order')]
    sidebar = build_sidebar(modules)

    page = TEMPLATE.replace('@@CSS@@', CSS)
    page = page.replace('@@JS@@', JS)
    page = page.replace('@@RES@@', RES)
    page = page.replace('@@SIDEBAR@@', sidebar)
    page = page.replace('@@COUNT@@', str(len(lessons)))
    page = page.replace('@@LESSONS@@', repr(lessons_html))
    page = page.replace('@@IDS@@', repr(lesson_ids))

    OUT.write_text(page, encoding='utf-8')
    print('OK:', OUT.name, '| размер:', round(OUT.stat().st_size / 1024 / 1024, 2), 'МБ')


if __name__ == '__main__':
    main()
