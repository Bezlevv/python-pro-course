---
title: Serverless: AWS Lambda и интеграции
summary: Событийные функции, локальная разработка, ограничения Lambda, интеграция с S3/API Gateway и тарифы.
order: 7
duration: 55 мин
difficulty: advanced
tags: aws, lambda, serverless, s3, api gateway
---

Serverless-подход позволяет запускать код без управления серверами: инфраструктура выделяется по требованию. В Python самый популярный сценарий — AWS Lambda.

## Что такое Lambda

Функция Lambda запускается на событие: HTTP-запрос (API Gateway), появление файла в S3, сообщение в очереди. Платят за время выполнения и количество вызовов.

## Структура функции

```python
def handler(event, context):
    name = event.get("name", "мир")
    return {"statusCode": 200, "body": f"Привет, {name}"}
```

`event` — словарь с данными события, `context` — окружение (тайм-ауты, память).

## Локальная разработка

AWS SAM (`sam local start-api`) и `aws-lambda-ric` позволяют запускать функции локально. Также удобен AWS Toolkit для VS Code.

## Ограничения

- Память до 10 ГБ, тайм-аут до 15 минут.
- Холодный старт: контейнер создаётся по требованию.
- Нет постоянного локального состояния — используйте S3 или БД.

## Интеграция с S3

Триггер «S3 → Lambda» запускает функцию при загрузке объекта (например, для ресайза изображений).

## Стратегия пакетов

Lambda поддерживает слои (layers) и контейнерные образы; зависимости укладывают в zip с `--python-path`.

## Итог урока

Serverless — способ просто запускать код, не думая о серверах. Lambda хороша для событийных задач: обработка файлов, вебхуки, малые API.

<!--TASK-->
### Задача 1 — Простая функция
Напиши handler, возвращающий `{"statusCode": 200, "body": "OK"}`. Вызови её вручную с `event = {}` и покажи результат.

### Задача 2 — Обработка HTTP-события
Напиши handler для API Gateway: принимает `event["queryStringParameters"]` и возвращает приветствие по имени из параметра name. Покажи вызов с event.

### Задача 3 — Локальный запуск через SAM
Установи AWS SAM CLI, опиши `template.yaml` (Resources: MyFunction, Properties: Runtime python3.13, Handler). Запусти `sam local invoke "MyFunction" -e event.json` и покажи вывод.

### Задача 4 — Чтение файла из S3
Напиши handler с событием от S3: по bucket/key достань объект через boto3, прочитай первые 100 символов и верни их. Добавь в комментарий, какие IAM-разрешения нужны.

### Задача 5 — Обработка ошибок
В handler добавь try/except: при исключении верни `{"statusCode": 500, "body": "Ошибка"}` и залогируй через print. Протестируй с неверным ключом.

### Задача 6 — Тест функции с моком boto3
Напиши pytest-тест, который через monkeypatch подменяет boto3.client("s3").get_object и проверяет, что handler возвращает содержимое. Убедись, что тест не ходит в облако.

### Задача 7 — Сравнение стоимости
Опиши (в комментарии) модель тарифов: сколько примерно стоило бы 1 млн вызовов функции с 128 МБ и 200 мс выполнения. Посчитай приблизительно на основе цены за 1 млн запросов и за ГБ-секунду.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Handler принимает (event, context); возврат — словарь.

### Подсказка 2
queryStringParameters может быть None — используй .get() с дефолтом.

### Подсказка 3
template.yaml: AWSTemplateFormatVersion, Resources, MyFunction: {Type: AWS::Serverless::Function, Properties: {CodeUri: ., Handler: app.handler, Runtime: python3.13}}.

### Подсказка 4
boto3.client("s3").get_object(Bucket=b, Key=k)["Body"].read().decode()[:100].

### Подсказка 5
В except: print("ERROR", e); return 500.

### Подсказка 6
Мок: monkeypatch.setattr("boto3.client", lambda *a, **k: FakeClient()) — отдай словарь с Body.

### Подсказка 7
Формула: стоимость = запросы × цена/1M + (ГБ-секунды) × цена/ГБ-с.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
```python
def handler(event, context):
    return {"statusCode": 200, "body": "OK"}

print(handler({}, None))
```
Вывод: {'statusCode': 200, 'body': 'OK'}.

### Разбор 2
```python
def handler(event, context):
    params = event.get("queryStringParameters") or {}
    name = params.get("name", "мир")
    return {"statusCode": 200, "body": f"Привет, {name}"}

event = {"queryStringParameters": {"name": "Аня"}}
print(handler(event, None))
```
Вывод: приветствие с именем.

### Разбор 3
```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: .
      Handler: app.handler
      Runtime: python3.13
```
```bash
sam local invoke "MyFunction" -e event.json
```
SAM собирает функцию локально и запускает с переданным событием.

### Разбор 4
```python
import boto3

def handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    body = boto3.client("s3").get_object(Bucket=bucket, Key=key)["Body"].read().decode()
    return body[:100]
```
Функции нужны права s3:GetObject (IAM-роль).

### Разбор 5
```python
def handler(event, context):
    try:
        data = event["key"]
        return {"statusCode": 200, "body": str(data)}
    except Exception as e:
        print("ERROR", e)
        return {"statusCode": 500, "body": "Ошибка"}
```
При отсутствии ключа — 500 и запись в лог.

### Разбор 6
```python
import pytest

class FakeS3:
    def get_object(self, **kwargs):
        return {"Body": type("B", (), {"read": lambda self: b"текст"})()}

def test_handler(monkeypatch):
    import boto3
    monkeypatch.setattr(boto3, "client", lambda *a, **k: FakeS3())
    from app import handler
    event = {"Records": [{"s3": {"bucket": {"name": "b"}, "object": {"key": "k"}}}]}
    assert handler(event, None) == "текст"
```
Тест не обращается к облаку — boto3 подменяется.

### Разбор 7
```python
# Допустим: 1M вызовов = $0.20, 1 ГБ-с = $0.0000166667
# 128 МБ = 0.125 ГБ, 200 мс = 0.0000002 ГБ-с (для 1 с)
# 1M × 0.2с = 200000 ГБ-с × 0.125 = 25000 ГБ-с
# итог ≈ 0.20 + 25000 × 0.0000166667 ≈ 0.62 $
```
Модель тарифов: запросы + время × память. Для маленьких функций — копейки.
<!--/SOLUTION-->

<!--QUIZ-->
Что такое AWS Lambda?
- Функция, выполняющаяся по событию без управления сервером
- Виртуальная машина
- Контейнер
- База данных
* Правильный ответ: Функция, выполняющаяся по событию без управления сервером
Serverless-вычисления.

Что такое «холодный старт»?
- Создание окружения при первом вызове
- Остановка функции
- Перезагрузка БД
- Прогрев сети
* Правильный ответ: Создание окружения при первом вызове
Он добавляет задержку.

Как передать имя в handler?
- Через event["queryStringParameters"]
- Через глобальную переменную
- Через context
- Через файл
* Правильный ответ: Через event["queryStringParameters"]
Для API Gateway данные приходят в event.

Какие права нужны для чтения S3?
- s3:GetObject
- s3:ListBuckets
- ec2:DescribeInstances
- Не нужны
* Правильный ответ: s3:GetObject
IAM-роль назначает разрешения.

Как тестировать handler без облака?
- Подменяя boto3 через monkeypatch
- Ожидая реального S3
- Через реальные запросы
- Никак
* Правильный ответ: Подменяя boto3 через monkeypatch
Фейковый клиент возвращает данные.

Что делает SAM CLI?
- Позволяет запускать Lambda локально
- Создаёт таблицы
- Деплоит веб-сайты
- Пишет тесты
* Правильный ответ: Позволяет запускать Lambda локально
sam local invoke эмулирует исполнение.

Какая максимальная длительность Lambda?
- 15 минут
- 1 час
- 5 минут
- Без ограничений
* Правильный ответ: 15 минут
Тайм-аут конфигурируется.

Зачем слои (layers)?
- Для переиспользования зависимостей между функциями
- Для ускорения сети
- Для шифрования
- Для логирования
* Правильный ответ: Для переиспользования зависимостей между функциями
Слои содержат библиотеки.

Что возвращает handler?
- Словарь (JSON-ответ)
- Строку всегда
- None обязательно
- Список
* Правильный ответ: Словарь (JSON-ответ)
Ожидаемая форма для API Gateway.

Как уменьшить холодный старт?
- Увеличить память, использовать provisioned concurrency
- Запретить вызовы
- Удалить функцию
- Меньше кода
* Правильный ответ: Увеличить память, использовать provisioned concurrency
Резервные среды устраняют ожидание.
<!--/QUIZ-->
