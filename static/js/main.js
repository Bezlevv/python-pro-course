/* PythonПро — фронтенд-скрипты */

(function () {
  'use strict';

  /* --- Тема (тёмная/светлая) --- */
  var themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    var applyTheme = function (theme) {
      document.documentElement.setAttribute('data-theme', theme);
      themeToggle.textContent = theme === 'light' ? '🌙' : '☀️';
    };
    var current = document.documentElement.getAttribute('data-theme') || 'dark';
    applyTheme(current);
    themeToggle.addEventListener('click', function () {
      var next = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
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
})();
