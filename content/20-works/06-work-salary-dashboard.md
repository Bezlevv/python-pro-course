---
title: Самостоятельная работа: дашборд анализа зарплат
summary: Анализ рынка зарплат на pandas и matplotlib: генерация данных, очистка, агрегации, визуализация и интерактивный дашборд на Streamlit.
order: 6
duration: 180 мин
difficulty: advanced
tags: pandas, matplotlib, streamlit, анализ данных, визуализация
---

# Самостоятельная работа: дашборд анализа зарплат

Привет! Это самостоятельная работа уровня advanced. За 180 минут ты пройдёшь полный конвейер аналитика данных: от генерации данных до интерактивного дашборда, который можно показать работодателю. Ты будешь работать с pandas, matplotlib и Streamlit — стеком, на котором строятся сотни реальных аналитических продуктов.

## Постановка задачи

HR-агентство «Карьера» собирает данные о зарплатах IT-специалистов по городам России. Данные лежат в CSV-файле, но в сыром виде: с пропусками, выбросами и неоднородными значениями. Агентство хочет получить аналитический отчёт и интерактивный дашборд, чтобы:

- понимать, как распределены зарплаты по городам и должностям;
- видеть связь зарплаты с опытом и форматом работы (офис/удалёнка);
- быстро фильтровать данные по нужным параметрам.

Тебе нужно построить полный пайплайн: **данные → очистка → агрегация → визуализация → дашборд**.

Исходных данных нет — ты сам их сгенерируешь скриптом. Это обычная практика: для разработки пайплайна нужен реалистичный датасет, и его можно создать синтетически с фиксированным зерном (`random.seed(42)`), чтобы результат был воспроизводим.

Требования к датасету `salaries.csv`:

- 600 записей, столбцы: `city` (5 городов: Москва, Санкт-Петербург, Новосибирск, Екатеринбург, Казань), `position` (Программист, Аналитик, DevOps, Тестировщик, Дизайнер), `experience_years` (целое от 0 до 25), `salary_rub` (от 40 000 до 350 000), `remote` («да»/«нет»);
- ~5% записей должны содержать пропуски в `salary_rub`, ~5% — в `city`, плюс несколько дублей строк;
- добавь 5–8 явных выбросов: зарплаты в 10 раз выше нормы или отрицательные значения.

Функциональные требования к работе:

1. Скрипт `make_data.py` генерирует CSV и печатает `df.info()`.
2. Очистка: пропуски, выбросы по методу IQR, дубликаты, приведение типов и строк к единому виду.
3. Агрегации: средние и медианные зарплаты по городам и должностям, по бакетам опыта; результат сохраняется в отдельные CSV.
4. Визуализация: минимум три графика (распределение зарплат, boxplot по городам, bar chart средних по должностям), сохранённые в PNG.
5. Дашборд на Streamlit: заголовок, фильтры (город, должность, опыт, удалёнка), метрики и интерактивные графики, пересчитывающиеся при изменении фильтров.

## Что ты повторишь

pandas: `read_csv`, `info`, `isna`, `dropna`, `fillna`, `drop_duplicates`, `groupby`, `agg`, `cut`, `quantile`, `to_csv`. matplotlib: `hist`, `boxplot`, `bar`, `savefig`, `subplots`. Streamlit: `title`, `selectbox`, `multiselect`, `slider`, `checkbox`, `metric`, `pyplot`, `dataframe`.

## План работы

Иди по этапам по порядку — каждый следующий опирается на предыдущий. В конце у тебя получится самостоятельный проект из трёх скриптов: `make_data.py`, `analysis.py`, `app.py`.

<!--TASK-->
### Задача 1
Создай скрипт `make_data.py`, который генерирует датасет `salaries.csv` и сохраняет его. Используй `random.seed(42)`, списки городов и должностей, разумную логику: зарплата зависит от города (Москва дороже), должности и опыта. Добавь ~5% пропусков в `salary_rub` и `city` (записывай пустую строку или `NaN`), 3–5 полных дублей строк и 5–8 выбросов (отрицательные значения или зарплаты в 10 раз выше нормы). Базовые зарплаты задай как целые числа от 40 000. В конце выведи `df.info()` и первые 5 строк. Ожидаемый результат: файл `salaries.csv` создан, при запуске печатается таблица из 600 строк и 5 столбцов.

### Задача 2
Создай скрипт `analysis.py` и напиши в нём функцию `load_and_clean(path)` которая загружает CSV и полностью очищает данные: убирает дубликаты (`drop_duplicates`), заполняет пропуски в `salary_rub` медианой столбца, а в `city` — модой (самым частым городом); убирает выбросы по методу IQR для `salary_rub` (ниже `Q1 - 1.5*IQR` и выше `Q3 + 1.5*IQR`); приводит `city`, `position`, `remote` к нижнему регистру с `strip()` и переводит `remote` в булев тип. Вызывай функцию с `sys.argv[1]` (или захардкодь путь) и печатай, сколько строк было и сколько стало. Ожидаемый результат: в отчёте видно, что после очистки количество строк уменьшилось, пропусков нет, а `df.dtypes` показывает правильные типы.

### Задача 3
В том же `analysis.py` добавь функцию `calculate_stats(df)`, которая считает агрегации: среднюю и медианную зарплату, количество записей и долю удалёнки по городам (`groupby("city").agg({...})`); то же по должностям; зарплату по бакетам опыта через `pd.cut(df["experience_years"], bins=[0, 2, 5, 10, 26], labels=["0-2", "3-5", "6-10", "11+"])`. Сохрани три итоговые таблицы в CSV: `stats_city.csv`, `stats_position.csv`, `stats_experience.csv`. Ожидаемый результат: файлы созданы, в каждом — осмысленные цифры (например, средняя зарплата программистов выше средней по датасету, а у Москвы — выше, чем у Казани).

### Задача 4
В `analysis.py` добавь функции визуализации: `plot_salary_distribution(df)` — гистограмма зарплат с 30 бинами и подписанными осями (сохрани в `hist_salary.png`); `plot_salary_by_city(df)` — boxplot зарплат по городам (`savefig("boxplot_city.png")`); `plot_salary_by_position(df)` — столбчатая диаграмма средних зарплат по должностям (`barplot_position.png`). Используй `matplotlib` с `plt.figure(figsize=(10, 6))`, `plt.tight_layout()` и `plt.savefig(...)`. Ожидаемый результат: три PNG-файла появляются в папке; графики читаемы: оси подписаны, есть заголовки, а на boxplot видны «усы» и выбросы.

### Задача 5
Создай `app.py` — дашборд на Streamlit. Внутри: `st.title`, загрузка и очистка данных (переиспользуй функции из `analysis.py`), сайдбар с фильтрами: `st.selectbox` для города (с вариантом «Все города»), `st.multiselect` для должностей, `st.slider` для диапазона опыта, `st.checkbox` «Только удалёнка». Основная область: три `st.metric` (средняя зарплата, медианная, количество записей), `st.dataframe` с отфильтрованными данными и три графика (пирог-гистограмма, boxplot, bar chart), пересчитываемые на отфильтрованном датафрейме. Ожидаемый результат: `streamlit run app.py` открывает дашборд в браузере, фильтры меняют цифры метрик и формы графиков.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Используй `random.randint` для зарплаты с базой от города и должности: например база для Москвы 120000, для остальных 80000; умножай на коэффициент должности (Программист 1.2, Аналитик 1.0, DevOps 1.3, Тестировщик 0.85, Дизайнер 0.9) и добавляй `experience_years * 3500`. Пропуски: после генерации пройдись по случайным индексам (`random.sample(range(600), 30)`) и обнули значения. Выбросы: просто присвой нескольким строкам значения 5000000 или -1000. Затем `pd.DataFrame(...).to_csv("salaries.csv", index=False)`.

### Подсказка 2
Порядок очистки важен: сначала `drop_duplicates()`, потом типы, потом пропуски, потом выбросы. Медиану считай `df["salary_rub"].median()`, моду — `df["city"].mode()[0]`. Для IQR: `q1 = df["salary_rub"].quantile(0.25)`, `q3 = df["salary_rub"].quantile(0.75)`, дальше `df[(df["salary_rub"] >= q1 - 1.5 * (q3 - q1)) & (df["salary_rub"] <= q3 + 1.5 * (q3 - q1))]`. Иначе заработные платы в 5 миллионов уничтожат всю статистику.

### Подсказка 3
`groupby("city").agg(salary_mean=("salary_rub", "mean"), salary_median=("salary_rub", "median"), count=("salary_rub", "size"), share_remote=("remote", "mean"))` — так получаются именованные столбцы одним вызовом. Для бакетов опыта не забудь, что `pd.cut` с `labels` требует `include_lowest=True` для включения нуля: `pd.cut(df["experience_years"], bins=[0, 2, 5, 10, 26], labels=["0-2", "3-5", "6-10", "11+"], include_lowest=True)`.

### Подсказка 4
Для гистограммы: `plt.hist(df["salary_rub"], bins=30, edgecolor="white")`. Для boxplot: `df.boxplot(column="salary_rub", by="city", figsize=(10, 6))` — но лучше через `plt.subplots()` + `ax.boxplot([...])` либо `df.boxplot(...)` и затем `plt.savefig("boxplot_city.png")`. Не забудь `plt.title`, `plt.xlabel`, `plt.ylabel` и `plt.tight_layout()` перед `savefig`. Проверь, что графики действительно создаются и открываются.

### Подсказка 5
Фильтрацию строй цепочкой условий: `mask = df["city"] == selected_city` (если не «Все города»), `mask &= df["position"].isin(selected_positions)` (если список непуст), `mask &= df["experience_years"].between(exp_min, exp_max)`, `mask &= df["remote"]` (если чекбокс включён), затем `filtered = df[mask]`. Для графиков передавай `filtered` в функции из задачи 4, но вместо `savefig` показывай `st.pyplot(plt.gcf())`. Метрики: `st.metric("Средняя зарплата", f"{filtered['salary_rub'].mean():,.0f} ₽")`.

<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Файл `make_data.py`:

```python
import random
import pandas as pd

random.seed(42)

CITIES = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]
POSITIONS = ["Программист", "Аналитик", "DevOps", "Тестировщик", "Дизайнер"]
CITY_BASE = {"Москва": 120000, "Санкт-Петербург": 100000,
             "Новосибирск": 85000, "Екатеринбург": 80000, "Казань": 75000}
POS_COEF = {"Программист": 1.2, "Аналитик": 1.0, "DevOps": 1.3,
            "Тестировщик": 0.85, "Дизайнер": 0.9}

rows = []
for _ in range(600):
    city = random.choice(CITIES)
    position = random.choice(POSITIONS)
    experience = random.randint(0, 25)
    salary = int(CITY_BASE[city] * POS_COEF[position] + experience * 3500
                 + random.randint(-8000, 8000))
    remote = "да" if random.random() < 0.4 else "нет"
    rows.append({"city": city, "position": position,
                 "experience_years": experience, "salary_rub": salary,
                 "remote": remote})

df = pd.DataFrame(rows)

# пропуски: 5% зарплат и 5% городов
for idx in random.sample(range(600), 30):
    df.at[idx, "salary_rub"] = None
for idx in random.sample(range(600), 30):
    df.at[idx, "city"] = None

# дубликаты
df = pd.concat([df, df.iloc[:4]], ignore_index=True)

# выбросы
df.at[500, "salary_rub"] = 5_000_000
df.at[501, "salary_rub"] = -1000
df.at[502, "salary_rub"] = 4_200_000
df.at[503, "salary_rub"] = -500
df.at[504, "salary_rub"] = 950_000

df.to_csv("salaries.csv", index=False)
print(df.info())
print(df.head())
```

Ключевая идея — детерминированность: `random.seed(42)` гарантирует, что при каждом запуске получится один и тот же датасет. Это важно для воспроизводимости: любой, кто запустит твой скрипт, увидит те же цифры. Логика генерации: база зависит от города, коэффициент — от должности, к результату прибавляется вклад опыта и небольшой шум `random.randint(-8000, 8000)`. Пропуски внедряются присваиванием `None` в случайные строки — pandas запишет их как пустые ячейки в CSV. Создание дублей через `pd.concat` с первыми четырьмя строками имитирует «размноженные» записи. Выбросы задаются явно — так мы знаем, что их ровно пять.

### Разбор 2
Файл `analysis.py`:

```python
import sys
import pandas as pd


def load_and_clean(path):
    df = pd.read_csv(path)
    original = len(df)

    df = df.drop_duplicates()

    df["city"] = df["city"].fillna(df["city"].mode()[0]).str.strip().str.lower()
    df["position"] = df["position"].str.strip()
    df["salary_rub"] = pd.to_numeric(df["salary_rub"], errors="coerce")
    df["salary_rub"] = df["salary_rub"].fillna(df["salary_rub"].median())
    df["remote"] = df["remote"].str.strip().str.lower().map({"да": True, "нет": False})

    q1 = df["salary_rub"].quantile(0.25)
    q3 = df["salary_rub"].quantile(0.75)
    iqr = q3 - q1
    df = df[(df["salary_rub"] >= q1 - 1.5 * iqr) &
            (df["salary_rub"] <= q3 + 1.5 * iqr)]

    print(f"Было строк: {original}, стало: {len(df)}")
    print(df.dtypes)
    return df


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "salaries.csv"
    load_and_clean(path)
```

Порядок операций принципиален. Сначала `drop_duplicates` — иначе дубликаты удвоят вес некоторых записей. Затем типы: `pd.to_numeric(..., errors="coerce")` превращает мусорные значения в `NaN`, а заполнение медианой (`fillna`) заменяет все пропуски — включая битые строки. Медиана устойчивее среднего для «затыкания» дыр. Мода для города: `df["city"].mode()[0]` — самый частый город. Строки приводятся к нижнему регистру со `strip()`: это защищает от вариантов «москва» vs «Москва». Выбросы убираются по IQR — стандартный статистический метод: всё, что дальше полутора межквартильных размахов от квартилей, считается аномалией. Приведённый фильтр делает это одной строкой с `&` (не забывай скобки — `&` для Series имеет приоритет ниже сравнений). Запуск: `python analysis.py salaries.csv`.

### Разбор 3
Добавляем агрегации в `analysis.py`:

```python
def calculate_stats(df):
    by_city = df.groupby("city").agg(
        salary_mean=("salary_rub", "mean"),
        salary_median=("salary_rub", "median"),
        count=("salary_rub", "size"),
        share_remote=("remote", "mean"),
    ).round(0).sort_values("salary_mean", ascending=False)
    by_city.to_csv("stats_city.csv")

    by_position = df.groupby("position").agg(
        salary_mean=("salary_rub", "mean"),
        salary_median=("salary_rub", "median"),
        count=("salary_rub", "size"),
    ).round(0).sort_values("salary_mean", ascending=False)
    by_position.to_csv("stats_position.csv")

    df = df.copy()
    df["experience_group"] = pd.cut(
        df["experience_years"],
        bins=[0, 2, 5, 10, 26],
        labels=["0-2", "3-5", "6-10", "11+"],
        include_lowest=True,
    )
    by_experience = df.groupby("experience_group", observed=True).agg(
        salary_mean=("salary_rub", "mean"),
        salary_median=("salary_rub", "median"),
        count=("salary_rub", "size"),
    ).round(0)
    by_experience.to_csv("stats_experience.csv")

    print(by_city)
    print(by_position)
    print(by_experience)
    return by_city, by_position, by_experience
```

`groupby().agg()` с именованными агрегатами — самый выразительный способ собрать сводную таблицу: `salary_mean=("salary_rub", "mean")` означает «столбец salary_mean = среднее по salary_rub». `size` считает количество записей, `mean` по булеву столбцу `remote` автоматически даёт долю удалёнки (False = 0, True = 1). Сортировка по средней зарплате делает таблицу сразу читаемой. `pd.cut` разбивает непрерывный опыт на бакеты; `include_lowest=True` включает ноль в первый интервал, а `observed=True` убирает предупреждение pandas о категориальных группах. Сохранение в CSV — через `to_csv`; эти файлы будут входом для дашборда и отчёта.

### Разбор 4
Добавляем визуализацию в `analysis.py`:

```python
import matplotlib.pyplot as plt


def plot_salary_distribution(df):
    plt.figure(figsize=(10, 6))
    plt.hist(df["salary_rub"], bins=30, edgecolor="white", color="#4C72B0")
    plt.title("Распределение зарплат")
    plt.xlabel("Зарплата, ₽")
    plt.ylabel("Количество записей")
    plt.tight_layout()
    plt.savefig("hist_salary.png")
    plt.close()


def plot_salary_by_city(df):
    plt.figure(figsize=(10, 6))
    df.boxplot(column="salary_rub", by="city")
    plt.title("Зарплаты по городам")
    plt.xlabel("Город")
    plt.ylabel("Зарплата, ₽")
    plt.tight_layout()
    plt.savefig("boxplot_city.png")
    plt.close()


def plot_salary_by_position(df):
    means = df.groupby("position")["salary_rub"].mean().sort_values()
    plt.figure(figsize=(10, 6))
    means.plot(kind="bar", color="#55A868")
    plt.title("Средняя зарплата по должностям")
    plt.xlabel("Должность")
    plt.ylabel("Средняя зарплата, ₽")
    plt.tight_layout()
    plt.savefig("barplot_position.png")
    plt.close()
```

Гистограмма с 30 бинами показывает форму распределения — после очистки она должна быть одновершинной, без «хвостов» от выбросов. Boxplot по городам наглядно сравнивает медианы (линия внутри ящика), межквартильный размах (ящик) и «усы» (разброс). Столбчатая диаграмма сортирует должности по средней зарплате; `sort_values()` сразу даёт восходящий порядок. Везде стоит `plt.close()` после `savefig`: без этого в Jupyter/Streamlit графики накладываются друг на друга. `tight_layout` предотвращает обрезание подписей.

### Разбор 5
Файл `app.py`:

```python
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from analysis import load_and_clean, plot_salary_distribution, \
    plot_salary_by_city, plot_salary_by_position

st.set_page_config(page_title="Зарплаты IT", layout="wide")
st.title("💼 Анализ зарплат IT-специалистов")

df = load_and_clean("salaries.csv")

st.sidebar.header("Фильтры")
cities = ["Все города"] + sorted(df["city"].unique().tolist())
selected_city = st.sidebar.selectbox("Город", cities)
positions = sorted(df["position"].unique().tolist())
selected_positions = st.sidebar.multiselect("Должности", positions, default=positions)
exp_min, exp_max = st.sidebar.slider(
    "Опыт, лет", 0, 25, (0, 25))
only_remote = st.sidebar.checkbox("Только удалёнка")

mask = pd.Series(True, index=df.index)
if selected_city != "Все города":
    mask &= df["city"] == selected_city.lower()
if selected_positions:
    mask &= df["position"].isin(selected_positions)
mask &= df["experience_years"].between(exp_min, exp_max)
if only_remote:
    mask &= df["remote"]

filtered = df[mask]

col1, col2, col3 = st.columns(3)
col1.metric("Средняя зарплата", f"{filtered['salary_rub'].mean():,.0f} ₽")
col2.metric("Медианная зарплата", f"{filtered['salary_rub'].median():,.0f} ₽")
col3.metric("Записей в выборке", f"{len(filtered)}")

st.dataframe(filtered)

fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.hist(filtered["salary_rub"], bins=30, edgecolor="white")
ax1.set_title("Распределение зарплат")
ax1.set_xlabel("Зарплата, ₽")
st.pyplot(fig1)

fig2, ax2 = plt.subplots(figsize=(8, 4))
filtered.boxplot(column="salary_rub", by="city", ax=ax2)
st.pyplot(fig2)

fig3, ax3 = plt.subplots(figsize=(8, 4))
filtered.groupby("position")["salary_rub"].mean().sort_values().plot(
    kind="bar", ax=ax3)
ax3.set_title("Средняя зарплата по должностям")
st.pyplot(fig3)
```

Дашборд переиспользует функции из `analysis.py` — так мы не дублируем код очистки. Фильтры строятся цепочкой: начальная маска — все `True`, дальше `&=` добавляет условия. `st.sidebar` группирует управление слева; `st.columns` размещает метрики в ряд; `st.dataframe` показывает сырую отфильтрованную таблицу. Графики рисуются на собственных `subplots` и показываются через `st.pyplot(fig)`. Обрати внимание: маска города сравнивается с `selected_city.lower()` — потому что очистка привела города к нижнему регистру. Запуск: `streamlit run app.py`, браузер откроет http://localhost:8501. Меняй фильтры — метрики и графики пересчитываются мгновенно.
<!--/SOLUTION-->

## Критерии оценки

| Критерий | Что проверяется | Баллы |
|---|---|---|
| Генерация данных | `salaries.csv` с 600 записями, пропусками, дублями и выбросами; `seed(42)` | 15 |
| Очистка | Дубликаты, пропуски, IQR, ниж, правильные типы; отчёт «было/стало» | 20 |
| Агрегации | Три CSV: по городам, должностям, бакетам опыта; корректные средние/медианы | 20 |
| Визуализация | Три PNG, подписанные оси, читаемые заголовки | 15 |
| Дашборд | Фильтры работают, метрики и графики пересчитываются | 25 |
| Аккуратность кода | Функции разделены, повторный код отсутствует, имена осмысленные | 5 |

Итого 100 баллов. Оценка: 90+ — «отлично», 75–89 — «хорошо», 60–74 — «удовлетворительно», меньше 60 — работа требует доработки.

## Что сдать

1. Скрипты: `make_data.py`, `analysis.py`, `app.py` (или один проект-папку).
2. Сгенерированные файлы: `salaries.csv`, три CSV со статистикой, три PNG-графика.
3. Скриншот дашборда с включёнными фильтрами (например, «Москва + Программист + опыт 5–10 лет») и скриншот консоли с выводом `load_and_clean` (было/стало).
4. Краткий README: как запустить генерацию, анализ и дашборд, какие зависимости установить (`pip install pandas matplotlib streamlit`).

<!--QUIZ-->
Что делает `random.seed(42)` в скрипте генерации данных?
- Обеспечивает случайность при каждом запуске
- Делает генерацию воспроизводимой: при каждом запуске — одинаковый датасет
- Задаёт размер датасета
- Ускоряет генерацию
* Правильный ответ: Делает генерацию воспроизводимой: при каждом запуске — одинаковый датасет
`seed` фиксирует состояние генератора случайных чисел — любой повторный запуск даст ровно те же данные.

Зачем в задаче пере1 данные были именно с выбросами и пропусками?
- Чтобы усложнить задачу
- Чтобы проверить, умеешь ли ты привести реальные «грязные» данные к рабочему виду
- Чтобы данные выглядели красиво
- Это случайность генератора
* Правильный ответ: Чтобы проверить, умеешь ли ты привести реальные «грязные» данные к рабочему виду
Реальные данные почти всегда содержат пропуски, дубликаты и аномалии — обработка таких случаев и есть работа аналитика.

Какой метод убирает выбросы в задаче?
- `drop_duplicates`
- Метод межквартильного размаха (IQR): границы Q1 − 1.5·IQR и Q3 + 1.5·IQR
- `fillna`
- `groupby`
* Правильный ответ: Метод межквартильного размаха (IQR): границы Q1 − 1.5·IQR и Q3 + 1.5·IQR
Всё, что выходит за эти границы, считается аномалией и удаляется из выборки.

Почему пропуски в зарплате заполняются медианой, а не средним?
- Медиана считается быстрее
- Медиана устойчива к выбросам и не смещается из-за аномальных значений
- Среднее не умеет работать с NaN
- Медиана всегда больше среднего
* Правильный ответ: Медиана устойчива к выбросам и не смещается из-за аномальных значений
Если в данных есть гигантские выбросы, среднее «раздуется», а медиана останется устойчивой мерой центра.

Что вернёт `df["city"].mode()[0]`, если в столбце есть пропуски?
- Первый город в списке
- Самый частый город (моду распределения)
- Последний город в списке
- None
* Правильный ответ: Самый частый город (моду распределения)
`mode()` возвращает массив самых частых значений, `[0]` берёт первое из них — стандартный способ заполнить пропуски категориального столбца.

Какой агрегат в `groupby().agg()` считает количество записей в группе?
- `"mean"`
- `"size"`
- `"first"`
- `"count"`
* Правильный ответ: `"size"`
`"size"` возвращает число строк в каждой группе, включая строки с NaN; `"count"` считает только непустые значения.

Что делает `pd.cut(df["experience_years"], bins=[0, 2, 5, 10, 26], labels=["0-2", "3-5", "6-10", "11+"], include_lowest=True)`?
- Делит опыт на 4 интервала и присваивает каждой строке метку интервала
- Считает средний опыт
- Удаляет опыт больше 26 лет
- Сортирует строки по опыту
* Правильный ответ: Делит опыт на 4 интервала и присваивает каждой строке метку интервала
`cut` превращает непрерывную переменную в категориальную; `include_lowest=True` включает границу 0 в первый интервал.

Какой виджет Streamlit служит для выбора нескольких должностей сразу?
- `st.selectbox`
- `st.multiselect`
- `st.slider`
- `st.radio`
* Правильный ответ: `st.multiselect`
`multiselect` позволяет выбрать произвольное подмножество вариантов — идеально для фильтра по должностям.

Что произойдёт с графиками, если фильтры не изменились, а `st.pyplot(fig)` вызван после `plt.savefig`?
- График не покажется
- Ничего страшного: `st.pyplot` показывает текущую фигуру matplotlib
- Будет ошибка выполнения
- Откроется новое окно
* Правильный ответ: Ничего страшного: `st.pyplot` показывает текущую фигуру matplotlib
`st.pyplot` отображает активную фигуру; в дашборде мы рисуем `subplots` и передаём фигуру в `st.pyplot(fig)`.
<!--/QUIZ-->
