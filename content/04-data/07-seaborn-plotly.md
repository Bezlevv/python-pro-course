---
title: Seaborn и Plotly
summary: Статистическая визуализация с Seaborn и интерактивные графики с Plotly.
order: 7
duration: 45 мин
difficulty: intermediate
tags: seaborn, plotly, визуализация, графики
---

Привет! В уроке про Matplotlib мы строили графики вручную, указывая каждую ось. Но для анализа данных часто удобнее высокоуровневые библиотеки: Seaborn умеет рисовать красивые статистические графики одной строкой, а Plotly делает интерактивные графики, которые можно открывать в браузере. Освоим обе.

## Установка и Seaborn

Установка: `pip install seaborn plotly`. Seaborn построен поверх Matplotlib: `sns.set_theme()` включает современную тему оформления. В библиотеку встроены учебные наборы данных, которые загружаются через `sns.load_dataset`, — например, знаменитые `tips` (чаевые в ресторане):

```python
import seaborn as sns
sns.set_theme()

tips = sns.load_dataset("tips")
print(tips.head())
```

В колонках: `total_bill` (сумма счёта), `tip` (чаевые), `sex`, `day`, `time` и другие.

## Основные графики Seaborn

**Точечный график с цветом по категории** — `relplot`:

```python
sns.relplot(data=tips, x="total_bill", y="tip",
            hue="time", style="sex", size="size")
```

`hue` раскрашивает точки по значению категории, `style` задаёт форму точек, `size` — размер.

**Гистограмма распределения** — `displot`:

```python
sns.displot(data=tips, x="total_bill", bins=30)
```

**Ящик с усами (boxplot)** — `catplot` с `kind="box"`:

```python
sns.catplot(data=tips, x="day", y="tip", hue="sex", kind="box")
```

**Тепловая карта корреляций** — `heatmap`:

```python
sns.heatmap(tips.select_dtypes("number").corr(), annot=True)
```

`annot=True` печатает значения корреляции прямо в клетках.

## Интерактивность: Plotly

Plotly строит графики, которые можно крутить, приближать и наводить курсор, чтобы увидеть значения, — это удобно для презентаций и дашбордов. Рекомендуемый верхний уровень — Plotly Express (`px`):

```python
import plotly.express as px

fig = px.scatter(tips, x="total_bill", y="tip",
                 color="time", size="size", hover_name="day")
fig.show()
```

`fig.show()` открывает интерактивный график в браузере (в Jupyter — прямо в ячейке). Ящики с усами строятся так:

```python
px.box(tips, x="day", y="tip", color="sex").show()
```

Сохранить график в автономный HTML-файл можно так:

```python
fig.write_html("tips.html")
```

Такой файл открывается в любом браузере — даже у человека, у которого нет Python.

## Что выбрать?

- Быстро посмотреть распределения и связи в процессе анализа → Seaborn (статика, PNG).
- Показать результат коллегам или клиенту, дать покрутить → Plotly (HTML).

Можно и комбинировать: Seaborn — для исследования, Plotly — для демонстрации результата.

## Итог урока

Мы научились:

- строить точечные графики, гистограммы, ящики с усами и тепловые карты в Seaborn;
- раскрашивать и группировать данные через `hue` и `kind`;
- создавать интерактивные графики Plotly Express;
- сохранять их в автономный HTML.

Теперь практика.

<!--TASK-->
### Задача 1
Используя набор `tips` из Seaborn, напиши программу, которая:

1. включает тему Seaborn и загружает `tips`;
2. строит ящик с усами: по X — `day`, по Y — `tip`, с `hue="sex"`, и сохраняет график в `tips_boxplot.png` через метод `savefig` объекта, который возвращает `sns.catplot`;
3. строит в Plotly Express интерактивный точечный график: X — `total_bill`, Y — `tip`, цвет — `time`, размер — `size`;
4. сохраняет его в `tips_scatter.html` и печатает сообщение `Готово: tips_boxplot.png и tips_scatter.html`.

Ожидаемый результат: в рабочей папке появляются два файла, в консоли — указанное сообщение.

### Задача 2
Напиши программу, которая:

1. загружает `tips` и включает тему Seaborn;
2. строит точечный график `sns.relplot`: X — `total_bill`, Y — `tip`, с `hue="time"`, `style="sex"`, `size="size"`;
3. сохраняет график в `tips_relplot.png` через `savefig` возвращённого объекта и закрывает фигуру через `plt.close(g.figure)`;
4. выводит сообщение `График сохранён: tips_relplot.png`.

### Задача 3
Напиши программу, которая:

1. загружает `tips` и включает тему Seaborn;
2. строит гистограмму распределения суммы счёта через `sns.displot` с `bins=30` и `kde=True`;
3. сохраняет график в `bill_distribution.png` и закрывает фигуру;
4. выводит среднюю сумму счёта, округлённую до двух знаков.

Ожидаемый вывод: файл `bill_distribution.png` и строка `Средний счёт: 19.79`.

### Задача 4
Напиши программу, которая:

1. загружает `tips` и включает тему Seaborn;
2. считает корреляцию числовых столбцов через `tips.select_dtypes("number").corr()`;
3. строит тепловую карту через `sns.heatmap(..., annot=True)`;
4. сохраняет рисунок в `tips_corr.png` (через `ax.figure.savefig`) и выводит сообщение `Тепловая карта сохранена: tips_corr.png`.

### Задача 5
Напиши программу, которая:

1. загружает `tips`;
2. строит в Plotly Express интерактивный ящик с усами: X — `day`, Y — `tip`, цвет — `sex`;
3. сохраняет его в `tips_box_plotly.html`;
4. выводит сообщение `Интерактивный ящик сохранён: tips_box_plotly.html`.

<!--/TASK-->

<!--HINT-->
### Подсказка 1
`g = sns.catplot(data=tips, x="day", y="tip", hue="sex", kind="box")`, затем `g.savefig("tips_boxplot.png")`. Для Plotly: `fig = px.scatter(tips, x="total_bill", y="tip", color="time", size="size")`, потом `fig.write_html("tips_scatter.html")`. В конце `print(...)`.

### Подсказка 2
`relplot` тоже возвращает объект `FacetGrid` — сохраняй через `g.savefig("tips_relplot.png")` и закрывай фигуру `plt.close(g.figure)`, чтобы Matplotlib не держал её в памяти. Не забудь `import matplotlib.pyplot as plt`.

### Подсказка 3
`sns.displot(data=tips, x="total_bill", bins=30, kde=True)` — гистограмма с кривой плотности. Среднее считается из самого DataFrame: `tips["total_bill"].mean()`.

### Подсказка 4
`corr = tips.select_dtypes("number").corr()` — матрица корреляций. График: `ax = sns.heatmap(corr, annot=True)`, затем `ax.set_title(...)` и `ax.figure.savefig("tips_corr.png")`.

### Подсказка 5
Ящик в Plotly Express: `fig = px.box(tips, x="day", y="tip", color="sex")`. Сохранение в HTML — `fig.write_html("tips_box_plotly.html")`. Никакие окна не появятся, файл откроется в браузере.

<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Полное решение:

```python
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

sns.set_theme()
tips = sns.load_dataset("tips")

g = sns.catplot(data=tips, x="day", y="tip",
                hue="sex", kind="box")
g.savefig("tips_boxplot.png")
plt.close(g.figure)

fig = px.scatter(tips, x="total_bill", y="tip",
                 color="time", size="size")
fig.write_html("tips_scatter.html")

print("Готово: tips_boxplot.png и tips_scatter.html")
```

Разберём по шагам. `sns.catplot(... kind="box")` рисует ящики с усами по дням недели; `hue="sex"` разбивает каждый день на две группы — мужчины и женщины. Функция возвращает объект `FacetGrid`, у которого есть метод `savefig` — именно он сохраняет весь рисунок в PNG. После сохранения закрываем фигуру через `plt.close(g.figure)`, чтобы Matplotlib не держал её в памяти.

Дальше `px.scatter` создаёт интерактивный точечный график: каждая точка — один чек из набора `tips`. `color="time"` красит обед и ужин разными цветами, `size="size"` — размер компании. `fig.write_html` записывает автономный HTML-файл со встроенным JavaScript: его можно переслать любому человеку, он откроется в браузере и останется интерактивным — точки можно приближать и наводить на них курсор.

Итого у нас два артефакта: статичный PNG для отчёта и интерактивный HTML для показа. Такой дуэт — стандартный паттерн в анализе данных: исследование делается в Seaborn, а демонстрация результата — в Plotly.

### Разбор 2
Полное решение:

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
tips = sns.load_dataset("tips")

g = sns.relplot(data=tips, x="total_bill", y="tip",
                hue="time", style="sex", size="size")
g.savefig("tips_relplot.png")
plt.close(g.figure)

print("График сохранён: tips_relplot.png")
```

Разберём по шагам. `sns.relplot` — универсальная функция для точечных графиков. `x="total_bill"` и `y="tip"` задают координаты точек, `hue="time"` раскрашивает обед и ужин разными цветами, `style="sex"` назначает мужчинам и женщинам разные формы маркеров, а `size="size"` кодирует размер компании величиной точки. Так на одном графике умещаются четыре измерения данных.

`relplot` возвращает `FacetGrid` — так же, как `catplot`. Поэтому сохранение идёт через `g.savefig("tips_relplot.png")`, а фигуру после этого закрывают через `plt.close(g.figure)`. Если этого не сделать, в конце программы Matplotlib может оставить неиспользованные окна открытыми.

Такой график — отличный первый шаг анализа: он сразу показывает, есть ли связь между суммой счёта и чаевыми, и отличаются ли паттерны у мужчин и женщин, днём и вечером.

### Разбор 3
Полное решение:

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
tips = sns.load_dataset("tips")

g = sns.displot(data=tips, x="total_bill", bins=30, kde=True)
g.savefig("bill_distribution.png")
plt.close(g.figure)

print(f"Средний счёт: {tips['total_bill'].mean():.2f}")
```

Разберём по шагам. `sns.displot(data=tips, x="total_bill", bins=30, kde=True)` строит гистограмму распределения суммы счёта: данные разбиваются на 30 корзин, а `kde=True` добавляет сглаженную кривую плотности, по которой удобно оценивать форму распределения. Подобно `catplot` и `relplot`, `displot` возвращает `FacetGrid`, поэтому сохранение выполняется через `g.savefig(...)`, а после — `plt.close(g.figure)`.

Средняя сумма счёта считается прямо из DataFrame: `tips["total_bill"].mean()` даёт 19.7859…, а формат `:.2f` округляет до 19.79. Гистограмма показывает, что большинство счетов — небольшие (до 20 долларов), а дальше распределение вытягивается длинным хвостом вправо. Такая картина типична для экономических данных: много маленьких значений и немного очень больших.

### Разбор 4
Полное решение:

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
tips = sns.load_dataset("tips")

corr = tips.select_dtypes("number").corr()
ax = sns.heatmap(corr, annot=True)
ax.set_title("Корреляция числовых признаков")
ax.figure.savefig("tips_corr.png")

print("Тепловая карта сохранена: tips_corr.png")
```

Разберём по шагам. `tips.select_dtypes("number")` оставляет только числовые столбцы (total_bill, tip, size), а `.corr()` считает попарные коэффициенты корреляции Пирсона — от −1 до 1. Единица означает идеальную прямую связь, ноль — отсутствие связи.

`sns.heatmap(corr, annot=True)` рисует тепловую карту: клетки окрашены по значению корреляции, а `annot=True` печатает сами числа внутри клеток. В отличие от `catplot`/`relplot`, `heatmap` возвращает обычную ось Matplotlib (`ax`), поэтому заголовок ставится через `ax.set_title(...)`, а сохранение — через `ax.figure.savefig(...)`, где `figure` — фигура, которой принадлежит ось.

На карте видно, что корреляция между суммой счёта и чаевыми около 0.68 — заметная положительная связь, а вот размер компании почти не связан с чаевыми. Тепловая карта корреляций — стандартный инструмент разведки: она мгновенно показывает, какие признаки связаны и какие стоит использовать в модели.

### Разбор 5
Полное решение:

```python
import seaborn as sns
import plotly.express as px

tips = sns.load_dataset("tips")

fig = px.box(tips, x="day", y="tip", color="sex")
fig.write_html("tips_box_plotly.html")

print("Интерактивный ящик сохранён: tips_box_plotly.html")
```

Разберём по шагам. `px.box(tips, x="day", y="tip", color="sex")` строит интерактивные ящики с усами: по оси X — дни недели, по Y — чаевые, а `color="sex"` делит каждый день на две серии — мужчины и женщины. На графике каждый ящик показывает медиану, квартили и выбросы, а при наведении курсора Plotly показывает точные значения.

`fig.write_html("tips_box_plotly.html")` сохраняет график в автономный HTML-файл со встроенным JavaScript — он открывается в любом браузере без установки Python. В отличие от Seaborn, где ящик — статичная картинка, здесь его можно приближать, перемещать и изучать отдельные точки.

Такой файл удобно отправлять коллегам и клиентам: получатель просто открывает его двойным кликом и может сам изучать данные. Это главное преимущество Plotly — интерактивность без необходимости устанавливать что-либо.

<!--/SOLUTION-->

<!--QUIZ-->
Что возвращает sns.catplot(...)?
- Объект FacetGrid с методом savefig
- Ничего, рисует сразу
- Объект matplotlib.Figure
* Правильный ответ: Объект FacetGrid с методом savefig
catplot возвращает FacetGrid — сетку графиков по категориям, которую можно сохранить через метод savefig.

Какой параметр отвечает за раскраску точек по категории в Plotly Express?
- legend
- color
- palette
* Правильный ответ: color
В Plotly Express категориальная переменная передаётся в параметр color, и Plotly сам назначит цвета и легенду.

Чем Plotly отличается от Seaborn?
- Plotly умеет только линейные графики
- Plotly создаёт интерактивные графики, которые можно открывать в браузере
- Plotly не умеет сохранять в файлы
* Правильный ответ: Plotly создаёт интерактивные графики, которые можно открывать в браузере
Графики Plotly можно приближать и наводить курсор; Seaborn выдаёт статичное изображение.

Что делает fig.write_html("tips.html")?
- Открывает график в окне
- Сохраняет интерактивный график в автономный HTML-файл
- Превращает график в PNG
* Правильный ответ: Сохраняет интерактивный график в автономный HTML-файл
Файл открывается в любом браузере без установки Python.

Зачем нужен параметр annot=True в sns.heatmap?
- Чтобы подписать оси
- Чтобы печатать значения корреляции прямо в клетках
- Чтобы увеличить размер карты
* Правильный ответ: Чтобы печатать значения корреляции прямо в клетках
С annot=True каждая клетка содержит число — так матрицу корреляций можно читать без наведения на неё.

Что кодирует параметр hue в seaborn?
- Размер точек
- Категориальную переменную, по которой раскрашиваются элементы
- Тип линии
* Правильный ответ: Категориальную переменную, по которой раскрашиваются элементы
hue берёт категориальную колонку и назначает каждому её значению свой цвет и легенду.

<!--/QUIZ-->
