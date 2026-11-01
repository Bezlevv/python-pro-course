---
title: Мастерство раскладки: Flexbox и Grid
summary: Два главных механизма современной раскладки — Flexbox для «во линии» и Grid для сеток, плюс адаптивные стратегии.
order: 4
duration: 50 мин
difficulty: advanced
tags: css, flexbox, grid, адаптивность, раскладка
---

Пришло время настоящей раскладки. Раньше верстальщики мучились с `float` и таблицами; сегодня есть два мощных механизма: **Flexbox** — для распределения элементов вдоль одной оси, и **CSS Grid** — для двумерных сеток. Освоив их, ты сверстаешь практически любой интерфейс.

## Flexbox: ось и распределение

Flexbox работает с «гибкими» элементами в контейнере. У контейнера (`display: flex`) есть главная ось (по умолчанию — горизонтальная) и поперечная.

```css
.nav {
    display: flex;
    justify-content: space-between; /* распределение по главной оси */
    align-items: center;            /* выравнивание по поперечной */
    gap: 16px;                       /* расстояние между элементами */
}
```

Ключевые свойства:

- `flex-direction` — `row` (по умолчанию), `column`, `row-reverse`, `column-reverse`;
- `justify-content` — распределение по главной оси: `flex-start`, `center`, `space-between`, `space-around`, `space-evenly`;
- `align-items` — выравнивание по поперечной оси: `stretch`, `center`, `flex-start`, `flex-end`;
- `flex-wrap: wrap` — перенос элементов на новую строку;
- `gap` — зазор между элементами (заменяет марджины);
- `flex-grow`, `flex-shrink`, `flex-basis` — как элементы растут, сжимаются и какой у них базовый размер.

Классический приём — центрирование одного элемента: контейнеру задают `display: flex; justify-content: center; align-items: center;`. Проще не бывает.

```css
.card-row {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}
.card {
    flex: 1 1 240px;  /* растёт, сжимается, база 240px */
}
```

## Grid: сетка в две оси

Grid делит контейнер на колонки и строки. Главная сила — `grid-template-columns`, где можно повторять колонки и использовать единицы `fr` (доли свободного места):

```css
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
}
```

Разберём: `repeat(auto-fit, ...)` — сколько колонок поместится, столько и будет; `minmax(220px, 1fr)` — каждая колонка минимум 220px, дальше растёт поровну. Это готовая адаптивная сетка без единого медиазапроса.

Явные сетки задаются перечислением колонок:

```css
.layout {
    display: grid;
    grid-template-columns: 200px 1fr 240px; /* боковые + контент */
    grid-template-areas:
        "header header header"
        "nav main sidebar"
        "footer footer footer";
    gap: 16px;
}
```

А элементы расставляются по именованным областям: `grid-area: header` (часто `grid-area: nav;` и т.д.). Это удобно для каркаса всей страницы.

## Flex или Grid?

Простой критерий:

- **Порядок вдоль одной оси** (меню, строка карточек, центрирование) — Flexbox.
- **Сетка в обе стороны или каркас страницы** (галерея, раскладка с колонками) — Grid.
- Хочешь, чтобы карточки занимали равную ширину и переносились — часто подходит и то, и другое, но Grid с `auto-fit` элегантнее.

Оба механизма легко комбинировать: Grid раскладывает секции всей страницы, а внутри секций работает Flexbox.

## Алгоритм выбора раскладки

Когда перед тобой стоит новая задача, задай себе три вопроса в таком порядке:

1. **Это одна ось?** Меню, строка кнопок, иконки в ряд, вертикальный список — бери Flexbox. Он создан для раскладки вдоль линии.
2. **Это двумерная сетка?** Карточки в несколько рядов, прайс-лист, календарь, каркас страницы с колонками — бери Grid. Он управляет и колонками, и строками одновременно.
3. **Это компонент внутри сетки?** Например, карточка в галерее, внутри которой текст и кнопка в одну строку. Тогда снаружи Grid, а внутри карточки — Flexbox.

Этот порядок избавляет от распространённой ошибки — пытаться сделать всё на одном механизме. Золотой стандарт современной вёрстки: Grid для «скелета» страницы, Flexbox для «мышц» — внутреннего наполнения компонентов. И не забывай: `gap` работает и там, и там, а `auto-fit` с `minmax` делает сетку адаптивной без единого медиазапроса.

## Адаптивные стратегии

- **Grid с `auto-fit`/`minmax`** — сетка сама подстраивается под ширину.
- **Flex с `flex-wrap: wrap` и `flex-basis`** — элементы переносятся.
- **Медиазапросы** — когда нужно перестроить каркас целиком: например, превратить трёхколоночную раскладку в одну колонку:

```css
@media (max-width: 800px) {
    .layout {
        grid-template-columns: 1fr;
        grid-template-areas:
            "header"
            "nav"
            "main"
            "sidebar"
            "footer";
    }
}
```

## Типичные ошибки

- Забыл `gap` и ставишь марджины каждому второму элементу — используй `gap`.
- Путаешь `justify-content` (главная ось) и `align-items` (поперечная).
- Делаешь фиксированные пиксельные ширины вместо `minmax`/`fr` — ломается адаптивность.
- Не задаёшь `flex-wrap: wrap`, и элементы вылезают за экран.

Теперь соберём всё это в практических задачах — от навигации до полноценного каркаса страницы с тестами.

<!--TASK-->
### Задача 1
Создай `layout-project/index.html` и `style.css`. Сверстай горизонтальную навигацию на Flexbox:

- `<nav class="nav">` содержит логотип (текст «Logo») и `<ul class="nav-links">` с четырьмя ссылками;
- контейнер `.nav` — `display: flex; justify-content: space-between; align-items: center;`;
- список `.nav-links` — `display: flex; gap: 24px;` и без маркеров (`list-style: none`).

Ожидаемый результат: логотип слева, ссылки справа, всё по центру по вертикали.

### Задача 2
Создай класс `.center` — блок, который центрирует содержимое и по горизонтали, и по вертикали (например, секция с текстом «Привет, мир!» на всю высоту окна: `min-height: 100vh`). Затем сверстай ряд карточек: контейнер `.card-row` с `display: flex; flex-wrap: wrap; gap: 20px;` и три карточки `.card` с `flex: 1 1 240px;`. Ожидаемый результат: на широком экране три карточки в ряд, при сужении они переносятся и занимают по ширине столько, сколько помещается.

### Задача 3
Сверстай адаптивную галерею на Grid: контейнер `.gallery` с `display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px;` и восемь карточек (класс `.card`, любое содержимое). Ожидаемый результат: при изменении ширины окна количество колонок меняется автоматически, без единого медиазапроса.

### Задача 4
Сверстай каркас страницы на Grid с именованными областями. Элементы: `<header class="site-header">`, `<nav class="sidebar">`, `<main class="content">`, `<aside class="aside">`, `<footer class="site-footer">`. Задай контейнеру `.layout`:

- `display: grid`;
- `grid-template-columns: 200px 1fr 240px`;
- `grid-template-areas` с областями `header header header`, `sidebar content aside`, `footer footer footer`;
- каждому элементу — `grid-area` с его именем.

Затем добавь медиазапрос: при `max-width: 800px` перестрой сетку в одну колонку (`grid-template-columns: 1fr`) и разложи области вертикально. Проверь в браузере: сузь окно — каркас должен перестроиться.

Дополнительно напиши pytest-тест `test_grid_layout.py`: рендерь `index.html` через jinja2 (`Environment().from_string(html).render()`) и проверь через `BeautifulSoup` наличие всех пяти элементов каркаса (`.layout`, `.site-header`, `.sidebar`, `.content`, `.aside`, `.site-footer`); затем прочитай `style.css` и проверь, что у класса `.layout` есть `grid-template-areas`, а внутри блока `@media (max-width: 800px)` — `grid-template-columns: 1fr`. Ожидаемый результат: все проверки проходят.

### Задача 5
Напиши pytest-тесты `test_layout.py`:

- тест HTML: прочитай `index.html` через `BeautifulSoup` и проверь наличие всех пяти элементов каркаса (`.layout`, `.site-header`, `.sidebar`, `.content`, `.aside`, `.site-footer`);
- тест CSS: прочитай `style.css` и проверь, что в нём есть `display: flex` и `display: grid`, `justify-content`, `align-items`, `gap`, `grid-template-columns`, `grid-template-areas`, `@media`;
- тест раскладки: убедись, что в CSS класс `.layout` использует `grid-template-areas`, а `.nav` использует `justify-content: space-between`;
- тест адаптивности: проверь, что внутри `@media (max-width: 800px)` есть `grid-template-columns: 1fr`.

Ожидаемый результат: все тесты проходят.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Вложенный flex: внешний `.nav` раскладывает логотип и список, а сам список `.nav-links` — тоже `display: flex` со ссылками. Не забудь `list-style: none` и `padding: 0` для списка.

### Подсказка 2
Центрирование: `.center { display: flex; justify-content: center; align-items: center; min-height: 100vh; }`. Для карточек: `.card-row { display: flex; flex-wrap: wrap; gap: 20px; }`, а `.card { flex: 1 1 240px; }` — это `flex-grow: 1; flex-shrink: 1; flex-basis: 240px`.

### Подсказка 3
Магия в одной строке: `grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));`. `auto-fit` создаёт столько колонок, сколько помещается, а `minmax(220px, 1fr)` гарантирует минимум 220px и равный рост. Добавь `gap: 16px`.

### Подсказка 4
Области задаются по строкам: `grid-template-areas: "header header header" "sidebar content aside" "footer footer footer";`. У каждого элемента свой `grid-area: header;` (и т.д.). Имена областей должны совпадать с `grid-area` элементов. В медиазапросe переопредели и `grid-template-columns`, и `grid-template-areas`. Для теста: вырезай блок `@media (max-width: 800px)` регулярным выражением `re.search(r"@media \(max-width: 800px\)\s*\{", css)` и проверяй `grid-template-columns: 1fr` в оставшейся части.

### Подсказка 5
Для проверки класса `layout` можно найти его блок в CSS регулярным выражением: `re.search(r"\.layout\s*\{([^}]*)\}", css)`. Итог — в группе 1. Проверяй `"grid-template-areas" in layout_block`. Для медиазапросa: `re.search(r"@media \(max-width: 800px\)\s*\{([^}]*)\}", css)`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
HTML:

```html
<nav class="nav">
    <span class="logo">Logo</span>
    <ul class="nav-links">
        <li><a href="#">Главная</a></li>
        <li><a href="#">Блог</a></li>
        <li><a href="#">Проекты</a></li>
        <li><a href="#">Контакты</a></li>
    </ul>
</nav>
```

CSS:

```css
.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
}
.nav-links {
    display: flex;
    gap: 24px;
    list-style: none;
    margin: 0;
    padding: 0;
}
```

Что здесь происходит? `.nav` становится flex-контейнером: `justify-content: space-between` раздвигает логотип и список к противоположным краям, `align-items: center` выравнивает их по вертикали. Внутри списка свой flex: ссылки идут в ряд с зазором `gap: 24px`. `list-style: none` убирает маркеры списка. Получилась классическая шапка сайта.

### Разбор 2
HTML:

```html
<section class="center">
    <p>Привет, мир!</p>
</section>

<div class="card-row">
    <div class="card">Карточка 1</div>
    <div class="card">Карточка 2</div>
    <div class="card">Карточка 3</div>
</div>
```

CSS:

```css
.center {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: #f0f4f8;
}
.card-row {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 24px;
}
.card {
    flex: 1 1 240px;
    background: #fff;
    border: 1px solid #e0e4ec;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
```

Что здесь происходит? Секция `.center` занимает минимум высоту окна и центрирует содержимое по обеим осям. В `.card-row` `flex-wrap: wrap` разрешает перенос, а `gap: 20px` задаёт зазоры. Каждая карточка имеет `flex: 1 1 240px`: база 240px, но при свободном месте она растёт (`grow: 1`), а при нехватке — сжимается (`shrink: 1`), не вылезая за экран.

### Разбор 3
HTML:

```html
<div class="gallery">
    <div class="card">1</div>
    <div class="card">2</div>
    <!-- ... всего 8 карточек -->
</div>
```

CSS:

```css
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    padding: 24px;
}
.card {
    background: #fff;
    border: 1px solid #e0e4ec;
    border-radius: 12px;
    padding: 40px;
    text-align: center;
}
```

Что здесь происходит? Grid считает, сколько колонок по минимум 220px помещается в контейнер, и создаёт ровно столько. Если окно сужается — колонок становится меньше, если расширяется — больше, и все они растут поровну благодаря `1fr`. Ни одного медиазапроса не нужно. Это идеальный рецепт галерей, каталогов и плиток.

### Разбор 4
HTML:

```html
<div class="layout">
    <header class="site-header">Шапка</header>
    <nav class="sidebar">Меню</nav>
    <main class="content">Контент</main>
    <aside class="aside">Боковая панель</aside>
    <footer class="site-footer">Подвал</footer>
</div>
```

CSS:

```css
.layout {
    display: grid;
    grid-template-columns: 200px 1fr 240px;
    grid-template-areas:
        "header header header"
        "sidebar content aside"
        "footer footer footer";
    gap: 16px;
    min-height: 100vh;
}
.site-header { grid-area: header; }
.sidebar    { grid-area: sidebar; }
.content     { grid-area: content; }
.aside      { grid-area: aside; }
.site-footer { grid-area: footer; }

@media (max-width: 800px) {
    .layout {
        grid-template-columns: 1fr;
        grid-template-areas:
            "header"
            "sidebar"
            "content"
            "aside"
            "footer";
    }
}
```

Файл `test_grid_layout.py`:

```python
import re
from bs4 import BeautifulSoup
from jinja2 import Environment


def render_index():
    with open("index.html", encoding="utf-8") as f:
        html = f.read()
    return Environment().from_string(html).render()


def test_layout_elements_exist():
    soup = BeautifulSoup(render_index(), "html.parser")
    for cls in ("layout", "site-header", "sidebar", "content", "aside", "site-footer"):
        assert soup.find(class_=cls) is not None, f"Нет класса {cls}"


def test_layout_uses_grid_areas():
    with open("style.css", encoding="utf-8") as f:
        css = f.read()
    m = re.search(r"\.layout\s*\{([^}]*)\}", css)
    assert m is not None
    assert "grid-template-areas" in m.group(1)


def test_media_switches_to_one_column():
    with open("style.css", encoding="utf-8") as f:
        css = f.read()
    m = re.search(r"@media \(max-width: 800px\)\s*\{", css)
    assert m is not None
    rest = css[m.end():]
    assert "grid-template-columns: 1fr" in rest
```

Что здесь происходит? Первый тест рендерит HTML через jinja2 и проверяет, что все пять элементов каркаса на месте. Второй вырезает тело правила `.layout` и убеждается, что каркас построен на `grid-template-areas`. Третий находит медиазапрос и проверяет, что после него встречается `grid-template-columns: 1fr` — значит, мобильная версия переключается на одну колонку. Теперь сам каркас: `grid-template-areas` описывает его строками: три колонки (`200px` — меню, `1fr` — контент, `240px` — панель) и три ряда. Каждый элемент получает имя области через `grid-area`. На узких экранах медиазапрос переопределяет и колонки (`1fr`), и области — всё выстраивается в одну колонку. Один CSS-файл держит две раскладки.

### Разбор 5
Файл `test_layout.py`:

```python
import re
from bs4 import BeautifulSoup


def read_css():
    with open("style.css", encoding="utf-8") as f:
        return f.read()


def css_block(selector):
    css = read_css()
    m = re.search(r"\.%s\s*\{([^}]*)\}" % selector, css)
    return m.group(1) if m else ""


def test_html_has_layout_elements():
    with open("index.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    for cls in ("layout", "site-header", "sidebar", "content", "aside", "site-footer"):
        assert soup.find(class_=cls) is not None, f"Нет класса {cls}"


def test_css_has_key_properties():
    css = read_css()
    for prop in ("display: flex", "display: grid", "justify-content",
                 "align-items", "gap", "grid-template-columns",
                 "grid-template-areas", "@media"):
        assert prop in css, f"Нет '{prop}'"


def test_nav_uses_space_between():
    assert "justify-content: space-between" in css_block("nav")


def test_layout_uses_grid_areas():
    assert "grid-template-areas" in css_block("layout")


def test_media_switches_to_one_column():
    css = read_css()
    m = re.search(r"@media \(max-width: 800px\)\s*\{", css)
    assert m is not None
    media_block = css[m.end():]
    assert "grid-template-columns: 1fr" in media_block
```

Что здесь происходит? `css_block()` вырезает тело правила по селектору — так мы проверяем свойства именно у конкретного класса, а не просто их наличие в файле. Тест `test_nav_uses_space_between` удостоверяется, что навигация использует правильное распределение; `test_layout_uses_grid_areas` — что каркас построен на областях. Последний тест находит медиазапрос, отрезает всё, что идёт после его открывающей скобки, и проверяет, что колонки переключаются на одну.
<!--/SOLUTION-->

<!--QUIZ-->
Какое свойство делает элемент flex-контейнером?
- display: flex
- position: flex
- flex: container
* Правильный ответ: display: flex
display: flex включает Flexbox-раскладку у контейнера.

Что делает justify-content: space-between?
- Центрирует элементы по вертикали
- Раздвигает элементы к краям, оставляя равные промежутки между ними
- Делает элементы одинаковой ширины
* Правильный ответ: Раздвигает элементы к краям, оставляя равные промежутки между ними
space-between раскладывает первый и последний элементы по краям, остальные — между ними.

Что задаёт gap?
- Зазор между элементами-соседями
- Отступ от края страницы
- Прозрачность элементов
* Правильный ответ: Зазор между элементами-соседями
gap — расстояние между элементами внутри flex/grid-контейнера.

Что означает flex: 1 1 240px?
- grow: 1, shrink: 1, basis: 240px
- Только задание базы в 240px
- Запрет на растягивание
* Правильный ответ: grow: 1, shrink: 1, basis: 240px
Сокращение задаёт три свойства: рост, сжатие и базовый размер.

Что делает grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))?
- Создаёт адаптивную сетку: сколько колонок помещается, столько и создаётся
- Создаёт ровно три колонки
- Запрещает перенос колонок
* Правильный ответ: Создаёт адаптивную сетку: сколько колонок помещается, столько и создаётся
auto-fit считает колонки по ширине контейнера, minmax задаёт их минимальный размер.

Что означает единица 1fr в гриде?
- Одна доля свободного пространства
- Один пиксель
- 1% ширины
* Правильный ответ: Одна доля свободного пространства
Единица fr распределяет свободное место пропорционально долям.

Для чего используются grid-template-areas?
- Чтобы дать имена областям сетки и расставить по ним элементы
- Чтобы задать цвета областей
- Чтобы объявить переменные
* Правильный ответ: Чтобы дать имена областям сетки и расставить по ним элементы
Области задаются строками, а элементы получают имена через grid-area.

Что выбрать для меню из ссылок в одну строку?
- Flexbox
- Grid с областями
- float
* Правильный ответ: Flexbox
Для одной оси — Flexbox; Grid лучше для двумерных сеток.

Что происходит при flex-wrap: wrap?
- Элементы переносятся на новую строку, если не помещаются
- Элементы сжимаются до 0
- Элементы скрываются
* Правильный ответ: Элементы переносятся на новую строку, если не помещаются
wrap разрешает перенос вместо сжатия в одну строку.

Как центрировать блок по обеим осям?
- display: flex; justify-content: center; align-items: center;
- text-align: center; margin: auto;
- display: block; width: 50%;
* Правильный ответ: display: flex; justify-content: center; align-items: center;
Оба свойства центрируют по главной и поперечной осям.
<!--/QUIZ-->
