---
title: Экзамен: Django REST Framework
summary: Проверь себя по всему модулю: сериализаторы, viewsets, JWT, фильтрация и тестирование.
order: 99
duration: 30 мин
difficulty: advanced
exam: true
tags: drf, экзамен
---

<!--QUIZ-->
Что делает класс Response в DRF?
- Формирует JSON-ответ с правильными заголовками
- Подключается к базе данных
- Рендерит HTML-страницы
* Правильный ответ: Формирует JSON-ответ с правильными заголовками
Response превращает объект в JSON и выставляет Content-Type и код состояния.

Какой метод нужно реализовать в базовом Serializer, чтобы создать объект?
- create(validated_data)
- save_object()
- insert()
* Правильный ответ: create(validated_data)
Метод create вызывается из save(), когда объекта ещё нет.

Что делает ModelSerializer автоматически?
- Генерирует поля, create() и update() из модели
- Создаёт базу данных
- Меняет схему таблиц
* Правильный ответ: Генерирует поля, create() и update() из модели
ModelSerializer строит поля по модели и умеет сохранять данные.

Какой класс объединяет весь CRUD в один класс?
- ModelViewSet
- APIView
- ListAPIView
* Правильный ответ: ModelViewSet
ModelViewSet содержит list, retrieve, create, update, partial_update, destroy.

Что делает DefaultRouter?
- Автоматически создаёт маршруты для ViewSet
- Генерирует миграции
- Проверяет пароли
* Правильный ответ: Автоматически создаёт маршруты для ViewSet
Router.register("books", BookViewSet) строит все стандартные URL.

Сколько живёт access-токен в SimpleJWT по умолчанию?
- 5 минут
- 30 дней
- 1 год
* Правильный ответ: 5 минут
По умолчанию — 5 минут, срок меняется через SIMPLE_JWT.

Какой класс прав разрешает доступ только залогиненным?
- IsAuthenticated
- AllowAny
- IsAdminReadOnly
* Правильный ответ: IsAuthenticated
IsAuthenticated пропускает только аутентифицированных пользователей.

Какой параметр использует SearchFilter?
- ?search=...
- ?filter=...
- ?find=...
* Правильный ответ: ?search=...
SearchFilter ищет подстроку по полям из search_fields.

Что содержит ключ count в ответе с пагинацией?
- Общее количество записей
- Номер страницы
- Размер страницы
* Правильный ответ: Общее количество записей
count — число записей во всей выборке, а не на странице.

Как залогинить клиента в APITestCase без запроса?
- client.force_authenticate(user=user)
- client.login(user=user)
- client.auth(user=user)
* Правильный ответ: client.force_authenticate(user=user)
force_authenticate напрямую вставляет пользователя в APIClient.
<!--/QUIZ-->
