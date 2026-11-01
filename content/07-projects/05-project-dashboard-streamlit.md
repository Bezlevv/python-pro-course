---
title: Проект: дашборд на Streamlit
summary: Строим интерактивный дашборд продаж: загрузка данных, метрики, графики и фильтры на Streamlit.
order: 5
duration: 60 мин
difficulty: intermediate
---

Привет! Streamlit — библиотека, которая превращает Python-скрипт в веб-приложение за минуты: не нужно писать HTML, CSS и JavaScript. В этом проекте мы построим дашборд продаж, который будет пересчитываться при движении ползунков и выборе фильтров.

## О проекте

Представь, что у небольшого магазина есть таблица продаж: дата, товар, категория, сумма. Мы сделаем страницу, где:

- вверху — ключевые метрики (общая выручка, число продаж, средний чек);
- ниже — линейный график выручки по дням;
- ещё ниже — фильтры: диапазон дат и выбор категории.

Любое изменение фильтра мгновенно перестраивает весь дашборд.

## План сборки

1. Установить Streamlit, Pandas и NumPy.
2. Сгенерировать данные о продажах.
3. Вывести таблицу и метрики.
4. Нарисовать графики.
5. Добавить виджеты-фильтры.
6. Добавить кэширование данных.
7. Запустить приложение.

## Шаг 1. Установка

```bash
pip install streamlit pandas numpy
```

## Шаг 2. Данные

Создадим демонстрационные данные за 90 дней — три категории товаров:

```python
import streamlit as st
import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=90)
categories = ["Электроника", "Одежда", "Книги"]

rows = []
for d in dates:
    for cat in categories:
        n = np.random.randint(1, 6)
        for _ in range(n):
            rows.append({
                "date": d,
                "category": cat,
                "amount": round(np.random.uniform(500, 15000), 2),
            })

df = pd.DataFrame(rows)
```

`pd.date_range` создаёт последовательность дат, `np.random` — случайные числа, `pd.DataFrame` собирает всё в таблицу. `seed(42)` делает данные воспроизводимыми.

## Шаг 3. Метрики

`st.metric` показывает значение с подписью:

```python
total = df["amount"].sum()
orders = len(df)
avg = df["amount"].mean()

st.metric("Выручка", f"{total:,.0f} ₽")
st.metric("Продаж", orders)
st.metric("Средний чек", f"{avg:,.0f} ₽")
```

## Шаг 4. Графики

Streamlit понимает DataFrame напрямую:

```python
daily = df.groupby("date")["amount"].sum()
st.line_chart(daily)

by_cat = df.groupby("category")["amount"].sum()
st.bar_chart(by_cat)
```

`groupby` группирует строки, `line_chart` и `bar_chart` строят графики без единой строки JavaScript-кода.

## Шаг 5. Виджеты-фильтры

Добавим выбор диапазона дат и категории:

```python
min_date, max_date = df["date"].min(), df["date"].max()
start, end = st.date_input("Период", value=(min_date, max_date))
category = st.selectbox("Категория", ["Все"] + sorted(df["category"].unique()))
```

Теперь отфильтруем данные:

```python
mask = (df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))
filtered = df[mask]
if category != "Все":
    filtered = filtered[filtered["category"] == category]
```

После этого метрики и графики строятся по `filtered` — так фильтры влияют на весь дашборд.

## Шаг 6. Кэширование

Генерация данных занимает время. Обернём её в функцию с `@st.cache_data` — Streamlit сохранит результат и не будет пересчитывать при каждом действии:

```python
@st.cache_data
def load_sales_data():
    ...  # весь код генерации
    return df
```

## Шаг 7. Запуск

```bash
streamlit run app.py
```

Откроется браузер с приложением. Когда меняешь фильтр, Streamlit перезапускает скрипт сверху вниз, но кэшированные функции не выполняются заново.

## Итог урока

Мы научились:

- генерировать данные с Pandas и NumPy;
- показывать метрики и графики;
- создавать виджеты и фильтровать данные;
- кэшировать вычисления.

<!--TASK-->
**Задача.** Собери дашборд по шагам, затем добавь:

1. Новую метрику «Максимальная покупка» — максимальная сумма в отфильтрованных данных.
2. Гистограмму распределения сумм покупок: `fig, ax = plt.subplots(); ax.hist(filtered["amount"], bins=20); st.pyplot(fig)` (нужен `import matplotlib.pyplot as plt`).
3. Таблицу топ-5 самых дорогих продаж через `st.dataframe`.

Ожидаемый результат: при изменении фильтров меняются все метрики, гистограмма и таблица.
<!--/TASK-->

<!--HINT-->
`st.pyplot` требует `import matplotlib.pyplot as plt`. Топ-5: `filtered.nlargest(5, "amount")`. Не забудь обновить секцию метрик, чтобы она использовала `filtered`, а не исходный `df`.
<!--/HINT-->

<!--SOLUTION-->
Полное решение (`app.py`):

```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


@st.cache_data
def load_sales_data():
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=90)
    categories = ["Электроника", "Одежда", "Книги"]
    rows = []
    for d in dates:
        for cat in categories:
            n = np.random.randint(1, 6)
            for _ in range(n):
                rows.append({
                    "date": d,
                    "category": cat,
                    "amount": round(np.random.uniform(500, 15000), 2),
                })
    return pd.DataFrame(rows)


st.title("Дашборд продаж")

df = load_sales_data()

min_date, max_date = df["date"].min(), df["date"].max()
start, end = st.date_input("Период", value=(min_date, max_date))
category = st.selectbox("Категория", ["Все"] + sorted(df["category"].unique()))

mask = (df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))
filtered = df[mask]
if category != "Все":
    filtered = filtered[filtered["category"] == category]

if filtered.empty:
    st.warning("Нет данных за выбранный период.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Выручка", f"{filtered['amount'].sum():,.0f} ₽")
col2.metric("Продаж", len(filtered))
col3.metric("Средний чек", f"{filtered['amount'].mean():,.0f} ₽")
col4.metric("Макс. покупка", f"{filtered['amount'].max():,.0f} ₽")

st.subheader("Динамика выручки")
daily = filtered.groupby("date")["amount"].sum()
st.line_chart(daily)

st.subheader("Распределение сумм покупок")
fig, ax = plt.subplots()
ax.hist(filtered["amount"], bins=20, color="#4C72B0")
ax.set_xlabel("Сумма, ₽")
ax.set_ylabel("Число покупок")
st.pyplot(fig)

st.subheader("Топ-5 самых дорогих продаж")
st.dataframe(filtered.nlargest(5, "amount"))
```

Разбор:

- `@st.cache_data` — данные генерируются один раз и переиспользуются при каждом перезапуске скрипта.
- Виджеты `st.date_input` и `st.selectbox` возвращают выбранные значения; маска `mask` отфильтровывает строки DataFrame по датам, затем — по категории.
- `st.columns(4)` разбивает верхнюю область на четыре колонки метрик.
- Если после фильтрации данных нет, `st.warning` и `st.stop` аккуратно завершают скрипт.
- Маplotlib-гистограмма строится обычным способом и показывается через `st.pyplot(fig)`.
- `nlargest(5, "amount")` возвращает пять наибольших сумм — Streamlit отображает DataFrame как сортируемую таблицу.

Запуск: `streamlit run app.py`.
<!--/SOLUTION-->
