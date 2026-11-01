/* PythonПро — фронтенд-скрипты */

(function () {
  'use strict';

  /* --- Тема (тёмная/светлая/AMOLED) --- */
  var themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    var THEMES = ['dark', 'light', 'amoled'];
    var THEME_ICONS = { dark: '🌙', light: '☀️', amoled: '🕶️' };
    var applyTheme = function (theme) {
      document.documentElement.setAttribute('data-theme', theme);
      themeToggle.textContent = THEME_ICONS[theme] || '🌙';
    };
    var current = document.documentElement.getAttribute('data-theme') || 'dark';
    applyTheme(current);
    themeToggle.addEventListener('click', function () {
      var idx = THEMES.indexOf(document.documentElement.getAttribute('data-theme'));
      var next = THEMES[(idx + 1) % THEMES.length];
      applyTheme(next);
      try { localStorage.setItem('pythonpro-theme', next); } catch (e) {}
    });
  }

  /* --- Мобильное меню --- */
  var burger = document.getElementById('burger');
  var nav = document.getElementById('mainNav');
  if (burger && nav) {
    burger.addEventListener('click', function () { nav.classList.toggle('open'); });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a, button')) nav.classList.remove('open');
    });
  }

  /* --- Копирование кода --- */
  function addCopyButtons() {
    document.querySelectorAll('.md-body pre').forEach(function (pre) {
      if (pre.querySelector('.copy-btn')) return;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'copy-btn';
      btn.textContent = 'Копировать';
      btn.addEventListener('click', function () {
        var code = pre.querySelector('code');
        var text = code ? code.innerText : pre.innerText;
        var done = function () {
          btn.textContent = 'Скопировано ✓';
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = 'Копировать';
            btn.classList.remove('copied');
          }, 1600);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text); done(); });
        } else {
          fallbackCopy(text);
          done();
        }
      });
      pre.appendChild(btn);
    });
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
  }

  document.addEventListener('DOMContentLoaded', addCopyButtons);

  /* --- CSRF --- */
  function getCsrf() {
    var el = document.querySelector('input[name=csrfmiddlewaretoken]');
    return el ? el.value : '';
  }

  function postJSON(url, data) {
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrf()
      },
      body: JSON.stringify(data)
    }).then(function (r) { return r.json(); });
  }

  /* --- Песочница --- */
  var runBtn = document.getElementById('sandboxRun');
  if (runBtn) {
    runBtn.addEventListener('click', function () {
      var codeEl = document.getElementById('sandboxCode');
      var outEl = document.getElementById('sandboxOutput');
      var statusEl = document.getElementById('sandboxStatus');
      var url = runBtn.dataset.url;
      if (!codeEl || !outEl) return;
      if (!url) return;
      outEl.classList.add('hidden');
      outEl.classList.remove('error');
      statusEl.textContent = 'Выполняется…';
      runBtn.disabled = true;
      postJSON(url, { code: codeEl.value }).then(function (res) {
        runBtn.disabled = false;
        statusEl.textContent = res.verdict || '';
        if (res.error) {
          outEl.textContent = 'Ошибка: ' + res.error;
          outEl.classList.add('error');
        } else if (res.output) {
          outEl.textContent = res.output;
        } else {
          outEl.textContent = '✓ Программа завершилась без вывода.';
        }
        outEl.classList.remove('hidden');
      }).catch(function () {
        runBtn.disabled = false;
        statusEl.textContent = 'Ошибка запроса';
      });
    });
  }

  /* --- Викторина --- */
  var quizBtn = document.getElementById('quizCheck');
  if (quizBtn) {
    quizBtn.addEventListener('click', function () {
      var questions = document.querySelectorAll('.quiz-question');
      var answers = [];
      questions.forEach(function (q) {
        var checked = q.querySelector('input[type=radio]:checked');
        answers.push(checked ? parseInt(checked.value, 10) : null);
      });
      var url = quizBtn.dataset.url;
      if (!url) return;
      var examForm = document.querySelector('#quizForm[data-exam]');
      var examWrap = document.getElementById('examPassWrap');
      postJSON(url, { answers: answers }).then(function (res) {
        var scoreEl = document.getElementById('quizScore');
        if (scoreEl) scoreEl.textContent = res.score + ' из ' + res.total;
        if (examForm && examWrap && res.total) {
          var pct = res.score / res.total * 100;
          examWrap.classList.toggle('hidden', pct < 80);
          if (pct < 80) {
            if (scoreEl) scoreEl.textContent += ' — нужно не менее 80% для сдачи';
          }
        }
        res.results.forEach(function (r, i) {
          var q = questions[i];
          if (!q) return;
          q.classList.remove('correct', 'incorrect');
          q.classList.add(r.correct ? 'correct' : 'incorrect');
          var fb = q.querySelector('.quiz-feedback');
          if (!fb) return;
          fb.className = 'quiz-feedback ' + (r.correct ? 'ok' : 'bad');
          if (r.correct) {
            fb.textContent = '✓ Верно! ' + (r.explanation || '');
          } else {
            fb.textContent = '✗ Неверно. ' + (r.explanation || 'Правильный ответ подсвечен.');
            var opts = q.querySelectorAll('.quiz-option input');
            if (opts[r.correct_index]) opts[r.correct_index].checked = true;
          }
        });
      });
    });
  }

  /* --- Автосохранение заметок --- */
  var noteText = document.getElementById('noteText');
  if (noteText) {
    var noteTimer = null;
    var noteStatus = document.getElementById('noteStatus');
    var noteUrl = noteText.dataset.url;
    noteText.addEventListener('input', function () {
      if (noteStatus) noteStatus.textContent = 'Сохранение…';
      clearTimeout(noteTimer);
      noteTimer = setTimeout(function () {
        if (!noteUrl) return;
        var fd = new FormData();
        fd.append('text', noteText.value);
        fd.append('csrfmiddlewaretoken', getCsrf());
        fetch(noteUrl, { method: 'POST', body: fd })
          .then(function (r) { return r.json(); })
          .then(function () {
            if (noteStatus) noteStatus.textContent = '✓ Сохранено';
          })
          .catch(function () {
            if (noteStatus) noteStatus.textContent = 'Ошибка сохранения';
          });
      }, 800);
    });
  }
  /* --- Автопроверка по тест-кейсам --- */
  var testsBtn = document.getElementById('testsRun');
  if (testsBtn) {
    testsBtn.addEventListener('click', function () {
      var codeEl = document.getElementById('sandboxCode');
      var outEl = document.getElementById('testsResults');
      var url = testsBtn.dataset.url;
      if (!codeEl || !outEl || !url) return;
      if (!codeEl.value.trim()) {
        outEl.textContent = 'Сначала напиши код в песочнице.';
        outEl.classList.remove('hidden');
        return;
      }
      outEl.classList.add('hidden');
      testsBtn.disabled = true;
      postJSON(url, { code: codeEl.value }).then(function (res) {
        testsBtn.disabled = false;
        if (res.error) {
          outEl.textContent = 'Ошибка: ' + res.error;
          outEl.classList.add('error');
        } else {
          outEl.classList.remove('error');
          var lines = res.results.map(function (r) {
            if (r.passed) return '✅ Тест ' + r.num + ' — OK';
            return '❌ Тест ' + r.num + ' — не пройден\nОжидалось:\n' + r.expected + '\nПолучено:\n' + (r.output || r.error || 'ничего');
          });
          outEl.textContent = (res.all_passed ? '🎉 Все тесты пройдены!' : 'Не все тесты пройдены.') + '\n\n' + lines.join('\n\n');
        }
        outEl.classList.remove('hidden');
      }).catch(function () {
        testsBtn.disabled = false;
        outEl.textContent = 'Ошибка запроса';
        outEl.classList.remove('hidden');
      });
    });
  }
})();
