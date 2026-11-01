---
title: Современный CSS: переменные, переходы, анимации
summary: CSS-переменные, каскад и специфичность, transition, keyframes-анимации и медиазапросы.
order: 3
duration: 45 мин
difficulty: intermediate
tags: css, переменные, анимации, transition, media-запросы
---

CSS (Cascading Style Sheets) отвечает за внешний вид страницы. В этом уроке ты перейдёшь от «покрасить текст» к по-настоящему современным стилям: переменным, которые позволяют менять всю тему сайта одной строкой, плавным переходам и анимациям.

## Селекторы и специфичность

Стиль применяется через **селекторы**: теги (`.h1`), классы (`.card`), id (`#header`), атрибуты (`[type="email"]`), псевдоклассы (`:hover`, `:focus`, `:nth-child(2)`) и псевдоэлементы (`::before`, `::after`).

Специфичность решает, какое правило победит при конфликте: id (самое сильное) > классы и атрибуты > теги. Полезное правило: используй классы, а не id — так стили легче переиспользовать.

```css
.card { /* класс — базовый уровень */
    background: #fff;
}
.card:hover { /* «:hover» — при наведении */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

## CSS-переменные (кастомные свойства)

Переменные объявляются внутри `:root` (псевдокласс корневого элемента — `html`) и используются через `var()`:

```css
:root {
    --color-primary: #3465e4;
    --color-text: #1f2430;
    --space: 8px;
}

.card {
    background: var(--color-primary);
    color: var(--color-text);
    padding: calc(var(--space) * 2);
}
```

Зачем это нужно? Один раз объявил цвет — и меняешь всю тему сайта в одном месте: `--color-primary: #e4345c`. `calc()` позволяет вычислять значения на лету, например `calc(100% - 40px)`.

## Псевдоклассы состояния

- `:hover` — наведение мыши;
- `:focus` — элемент в фокусе (клавиатура);
- `:focus-visible` — фокус, видимый пользователю (современный стандарт);
- `:active` — момент нажатия;
- `:nth-child(n)` — порядковый номер среди соседей.

Важно: состояние `:hover` на телефонах не существует, а `:focus` — важнейший сигнал для доступности. Никогда не убирай фокус полностью (`outline: none` без замены) — это ломает клавиатурную навигацию.

## Переходы transition

`transition` плавно меняет свойства между состояниями. Короткая запись: `transition: property duration timing-function delay`.

```css
.btn {
    background: var(--color-primary);
    transition: background 0.3s ease, transform 0.3s ease;
}
.btn:hover {
    background: #1e3f8f;
    transform: translateY(-2px);
}
```

Анимировать стоит только свойства, которые браузер «умеет» анимировать дешёво: `transform`, `opacity`, цвета, `box-shadow`. Не анимируй `width` и `height` — это дёргано и медленно.

## Анимации keyframes

Если переход — это реакция на действие, то `@keyframes` — сценарий, который выполняется сам. Объявляешь кадры и подключаешь их через `animation`:

```css
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-title {
    animation: fadeInUp 0.8s ease-out both;
}
```

`both` в конце значит: до старта и после конца анимации применяются кадры `from`/`to` (элемент не «прыгает»).

## Медиазапросы

`@media` применяет стили при выполнении условия — размер экрана, ориентация, настройки пользователя:

```css
/* Базовые стили — для всех */

@media (max-width: 600px) {
    .hero-title {
        font-size: 28px;
    }
    .sidebar { display: none; }
}

/* Тёмная тема системы */
@media (prefers-color-scheme: dark) {
    :root {
        --color-text: #e8eaf0;
    }
}

/* Пользователь просил меньше движения */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

Правило: **сначала базовые стили, потом `@media`**. `prefers-reduced-motion` — обязательная вежливость: для людей с вестибулярными нарушениями отключаем анимации.

## Порядок работы

1. Структура и переменные — `:root`.
2. Базовые стили элементов.
3. Оформление компонентов классами.
4. Состояния (`:hover`, `:focus-visible`).
5. Переходы и анимации.
6. Медиазапросы в конце.

Теперь закрепим: ты соберёшь страницу с переменными, плавными кнопками, анимацией и адаптивностью, а затем напишешь тесты, которые проверяют сами стили и их связь с HTML.

<!--TASK-->
### Задача 1
Создай папку `css-project/` и в ней файлы `index.html` и `style.css`. В `style.css` объяви в `:root` переменные: `--color-primary: #3465e4`, `--color-secondary: #2a9d8f`, `--color-background: #f5f7fa`, `--color-text: #1f2430`, `--radius: 12px`. Затем оформи простую страницу: карточку (класс `.card`) с белё фоном, скруглением `var(--radius)` и рамкой; заголовок с цветом `var(--color-primary)`; кнопку (класс `.btn`) с фоном `var(--color-primary)`. Подключи `style.css` в `index.html` через `<link rel="stylesheet" href="style.css">`. Открой в браузере — цвета должны совпадать с переменными.

### Задача 2
Добавь эффекты наведения. Кнопке дай:

- плавный переход `transition: background 0.3s ease, transform 0.3s ease`;
- при `:hover` — затемнение фона (например, `#1e3f8f`) и подъём `transform: translateY(-2px)`;
- при `:focus-visible` — заметное кольцо `outline: 3px solid #ffb703; outline-offset: 2px;`.

Карточке добавь тень при наведении и переход тени. Проверь: при наведении и при передвижении по странице клавишей `Tab` всё должно меняться плавно.

### Задача 3
Создай баннер вверху страницы (класс `.hero`) с заголовком (класс `.hero-title`) и подзаголовком. Добавь анимацию появления:

- `@keyframes fadeInUp` — от `opacity: 0; transform: translateY(20px)` к `opacity: 1; transform: translateY(0)`;
- заголовок и подзаголовок получают `animation: fadeInUp 0.8s ease-out both`, с задержкой подзаголовка `animation-delay: 0.2s`.

Добавь также `@media (prefers-reduced-motion: reduce)`, который почти полностью отключает анимации и переходы.

### Задача 4
Сделай страницу адаптивной: добавь медиазапросы:

- при `max-width: 600px` уменьши размер шрифта заголовка до `26px`, скрой боковую колонку (класс `.sidebar`, добавь её в HTML с любым текстом);
- при `prefers-color-scheme: dark` переопредели `--color-background` на `#16181d`, `--color-text` на `#e8eaf0`, `--color-primary` на `#6b9aff`.

Проверь в браузере: сузь окно до мобильного размера, включи тёмную тему системы (если браузер поддерживает) — страница должна реагировать.

Затем напиши pytest-тест `test_responsive.py`: прочитай `index.html` и отрендерь его через jinja2 (`env.from_string(html)`), разбери через `BeautifulSoup` и проверь, что на странице есть элемент с классом `sidebar`. После этого прочитай `style.css` и проверь, что в нём есть `@media (max-width: 600px)`, правило `display: none` для `.sidebar` и блок `prefers-color-scheme: dark` с переопределением переменных `--color-background` и `--color-text`. Ожидаемый результат: все проверки теста проходят.

### Задача 5
Напиши pytest-тесты `test_css.py`:

- тест `style.css`: прочитай файл как текст и проверь наличие `:root`, минимум трёх переменных `--color-`, использования `var(` в правилах, `transition` у `.btn`, `@keyframes fadeInUp` и `@media`;
- тест рендера: отрендерь через jinja2 шаблон `index.html` (просто текст без переменных — можно читать файл) и проверь через `BeautifulSoup`, что на странице есть `<link rel="stylesheet" href="style.css">` и элементы с классами `card`, `btn` и `hero-title`;
- тест связи: собери из CSS-файла все классы (по регулярному выражению `\.([a-z-]+)\s*\{`) и убедись, что каждый класс из HTML (`card`, `btn`, `hero`, `hero-title`, `sidebar`) присутствует в CSS.

Ожидаемый результат: все три теста проходят.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Переменные объявляются как `--имя: значение;` внутри `:root { ... }`, а используются как `var(--имя)`. В `index.html` обязательно подключи стили в `<head>`: `<link rel="stylesheet" href="style.css">`. Не забудь `<meta name="viewport" ...>`.

### Подсказка 2
`:` — это сокращение: `transition: background 0.3s ease, transform 0.3s ease`. Чтобы не потерять `:focus` при использовании мыши, задай `:focus-visible` отдельно от `:hover`. Тень: `box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15)`.

### Подсказка 3
Ключевые кадры: `@keyframes fadeInUp { from { ... } to { ... } }`. Подключение: `animation: fadeInUp 0.8s ease-out both`. Для второго элемента добавь `animation-delay: 0.2s` — и обязательно `animation-fill-mode: both` (иначе до старта элемент виден).

### Подсказка 4
Пиши медиазапросы после основных правил. Синтаксис: `@media (max-width: 600px) { ... }`. Для тёмной темы: `@media (prefers-color-scheme: dark) { :root { --color-background: #16181d; } }`. Для теста: `env.from_string(html).render()` вернёт ту же строку — это рендер через jinja2; дальше работай с BeautifulSoup. Проверку `display: none` для `.sidebar` делай по CSS: найди блок `@media (max-width: 600px)` и убедись, что внутри есть `.sidebar { display: none; }`.

### Подсказка 5
Чтение файла: `with open("style.css", encoding="utf-8") as f: css = f.read()`. Проверка наличия: `assert ":root" in css`. Классы из CSS: `re.findall(r"\.([a-z-]+)\s*\{", css)`. Для рендера через jinja2: `env = Environment(autoescape=True); template = env.from_string(html_text)` — или просто парси `index.html` напрямую через BeautifulSoup.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Файл `style.css`:

```css
:root {
    --color-primary: #3465e4;
    --color-secondary: #2a9d8f;
    --color-background: #f5f7fa;
    --color-text: #1f2430;
    --radius: 12px;
}

body {
    background: var(--color-background);
    color: var(--color-text);
    font-family: Arial, sans-serif;
}

.card {
    background: #fff;
    border: 1px solid #e0e4ec;
    border-radius: var(--radius);
    padding: 24px;
}

h1, h2 { color: var(--color-primary); }

.btn {
    background: var(--color-primary);
    color: #fff;
    border: none;
    border-radius: var(--radius);
    padding: 12px 24px;
    cursor: pointer;
}
```

В `index.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS-проект</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="card">
        <h1>Привет, CSS!</h1>
        <p>Это карточка с переменными.</p>
        <button class="btn">Нажми</button>
    </div>
</body>
</html>
```

Что здесь происходит? Все цвета и радиус объявлены в `:root` как переменные, а элементы используют `var(...)`. Теперь, чтобы поменять всю палитру, достаточно изменить значения в одном месте — `:root`. Такой подход называется «дизайн-токены».

### Разбор 2
Дополняем `style.css`:

```css
.btn {
    background: var(--color-primary);
    color: #fff;
    border: none;
    border-radius: var(--radius);
    padding: 12px 24px;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.3s ease;
}
.btn:hover {
    background: #1e3f8f;
    transform: translateY(-2px);
}
.btn:focus-visible {
    outline: 3px solid #ffb703;
    outline-offset: 2px;
}
.card {
    background: #fff;
    border-radius: var(--radius);
    padding: 24px;
    transition: box-shadow 0.3s ease;
}
.card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

Что здесь происходит? `transition` описывает, что и как долго будет плавно меняться: фон и сдвиг — за 0.3s. На `:hover` меняются конечные значения, и браузер анимирует переход. `:focus-visible` срабатывает только когда фокус действительно нужно показать (например, при навигации клавиатурой) — это требование доступности. Тень карточки тоже переходит плавно, потому что у неё объявлен `transition: box-shadow`.

### Разбор 3
Добавляем баннер и анимацию:

```css
.hero {
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    color: #fff;
    padding: 48px;
    border-radius: var(--radius);
}

.hero-title {
    font-size: 36px;
    margin: 0;
    animation: fadeInUp 0.8s ease-out both;
}
.hero-subtitle {
    animation: fadeInUp 0.8s ease-out 0.2s both;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-delay: 0s !important;
        transition-duration: 0.01ms !important;
    }
}
```

Что здесь происходит? `@keyframes fadeInUp` описывает два кадра: старт (прозрачный, сдвинут вниз) и финиш (видимый, на месте). `animation: fadeInUp 0.8s ease-out both` подключает сценарий; `both` (это `animation-fill-mode: both`) применяет стартовый кадр до начала и финальный после конца — элемент не мигает. У подзаголовка задержка `0.2s` — он появляется вслед за заголовком. Медиазапрос `prefers-reduced-motion` сокращает анимации до миллисекунд для тех, кто их отключил в системе.

### Разбор 4
Добавляем адаптивность:

```css
@media (max-width: 600px) {
    .hero-title { font-size: 26px; }
    .sidebar { display: none; }
}

@media (prefers-color-scheme: dark) {
    :root {
        --color-background: #16181d;
        --color-text: #e8eaf0;
        --color-primary: #6b9aff;
    }
}
```

Файл `test_responsive.py`:

```python
import re
from bs4 import BeautifulSoup
from jinja2 import Environment


def render_index():
    with open("index.html", encoding="utf-8") as f:
        html = f.read()
    return Environment().from_string(html).render()


def test_has_sidebar_element():
    soup = BeautifulSoup(render_index(), "html.parser")
    assert soup.find(class_="sidebar") is not None


def test_media_queries_present():
    with open("style.css", encoding="utf-8") as f:
        css = f.read()
    assert "@media (max-width: 600px)" in css
    assert "@media (prefers-color-scheme: dark)" in css
    assert "--color-background" in css and "--color-text" in css


def test_sidebar_hidden_on_mobile():
    with open("style.css", encoding="utf-8") as f:
        css = f.read()
    m = re.search(r"@media \(max-width: 600px\)\s*\{([^}]*)\}", css)
    assert m is not None
    assert "display: none" in m.group(1)
    assert ".sidebar" in m.group(1)
```

Что здесь происходит? Первый тест подтверждает, что класс `sidebar` реально есть в HTML — значит, медиазапросу есть что скрывать. Второй проверяет наличие обоих медиазапросов и переменных тёмной темы. Третий вырезает тело мобильного медиазапроса регулярным выражением и убеждается, что внутри него `.sidebar` действительно скрывается через `display: none`. Это контроль «поведения» CSS, а не только его наличия.

Теперь разберём остальные части адаптивного задания. На экранах уже 600px заголовок уменьшается, а боковая колонка скрывается — типичное поведение для мобильных. А `prefers-color-scheme: dark` переопределяет переменные, когда в системе включена тёмная тема: фон становится тёмным, текст светлым, фирменный цвет светлеет для контраста. Красота переменных в том, что теперь переопределение в `:root` автоматически перекрашивает все элементы, которые используют `var()`.

### Разбор 5
Файл `test_css.py`:

```python
import re
from bs4 import BeautifulSoup


def read_css():
    with open("style.css", encoding="utf-8") as f:
        return f.read()


def test_css_has_variables_and_keywords():
    css = read_css()
    assert ":root" in css
    assert len(re.findall(r"--color-[a-z-]+:", css)) >= 3
    assert "var(" in css
    assert "transition:" in css
    assert "@keyframes fadeInUp" in css
    assert "@media" in css


def test_html_links_css_and_has_classes():
    with open("index.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    link = soup.find("link", rel="stylesheet")
    assert link is not None and link.get("href") == "style.css"
    for cls in ("card", "btn", "hero", "hero-title", "sidebar"):
        assert soup.find(class_=cls) is not None, f"Нет класса {cls}"


def test_html_classes_defined_in_css():
    css = read_css()
    css_classes = set(re.findall(r"\.([a-z-]+)\s*\{", css))
    with open("index.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    for element in soup.find_all(class_=True):
        for cls in element.get("class"):
            assert cls in css_classes, f"Класс {cls} не определён в CSS"
```

Что здесь происходит? Первый тест читает CSS как текст и ищет ключевые конструкции: `:root`, минимум три переменные, `var()`, `transition`, `@keyframes` и `@media`. Второй тест проверяет, что страница подключает правильный `style.css` и содержит нужные классы. Третий (и самый интересный) собирает все имена классов из CSS регулярным выражением и проверяет, что каждый класс, использованный в HTML, действительно определён в стилях. Если в CSS забыть класс — тест упадёт.
<!--/SOLUTION-->

<!--QUIZ-->
Где объявляются CSS-переменные, чтобы были доступны всем элементам?
- В селекторе body
- В :root
- В каждом классе отдельно
* Правильный ответ: В :root
:root — псевдокласс корневого элемента, переменные оттуда видны всем.

Как использовать CSS-переменную?
- var(--имя)
- get(--имя)
- use(--имя)
* Правильный ответ: var(--имя)
Значение переменной подставляется через var(--имя).

Что делает transition?
- Меняет цвет элемента мгновенно
- Плавно анимирует изменение свойств между состояниями
- Создаёт новые стили
* Правильный ответ: Плавно анимирует изменение свойств между состояниями
transition задаёт плавный переход при смене свойств.

Что такое @keyframes?
- Способ задать шрифт
- Сценарий анимации: набор кадров с промежуточными состояниями
- Тип селектора
* Правильный ответ: Сценарий анимации: набор кадров с промежуточными состояниями
@keyframes описывает, как меняется элемент во времени.

Какой псевдокласс срабатывает при фокусе с клавиатуры?
- :hover
- :focus-visible
- :active
* Правильный ответ: :focus-visible
:focus-visible показывает фокус только когда он важен (обычно клавиатура).

Что делает @media (max-width: 600px)?
- Применяет стили на экранах не шире 600px
- Увеличивает шрифт до 600px
- Скрывает все элементы
* Правильный ответ: Применяет стили на экранах не шире 600px
Это медиазапрос — стили внутри действуют только для узких экранов.

Для чего нужен prefers-reduced-motion?
- Чтобы ускорить анимации
- Чтобы отключить или сократить анимации для пользователей, которые этого просят
- Чтобы включить анимации на старых браузерах
* Правильный ответ: Чтобы отключить или сократить анимации для пользователей, которые этого просят
Это уважение к пользователям с вестибулярными нарушениями.

Какие свойства безопасно и дёшево анимировать?
- width и height
- transform и opacity
- font-size и padding
* Правильный ответ: transform и opacity
transform и opacity анимируются на GPU и не вызывают перекомпоновку страницы.

Что делает calc(100% - 40px)?
- Вычисляет значение на лету
- Округляет число
- Объявляет переменную
* Правильный ответ: Вычисляет значение на лету
calc() позволяет комбинировать единицы и вычислять размеры.

Что означает fill-mode: both в анимации?
- Анимация проигрывается дважды
- До старта и после конца применяются кадры from/to — элемент не «прыгает»
- Элемент исчезает после анимации
* Правильный ответ: До старта и после конца применяются кадры from/to — элемент не «прыгает»
both применяет стартовый кадр до начала и финальный после окончания.
<!--/QUIZ-->
