---
title: Экзамен: Крутые фишки
summary: Проверь знания автоматизации: pathlib/shutil, Telegram Bot API, QR-коды и Pillow, openpyxl/python-docx, мониторинг с requests/smtplib, генераторы на secrets.
order: 99
duration: 30 мин
difficulty: advanced
tags: экзамен
exam: true
---

<!--QUIZ-->
Какой метод pathlib создаёт папку и не падает, если она уже существует?
- mkdir()
- mkdir(parents=True, exist_ok=True)
- create()
- newdir()
* Правильный ответ: mkdir(parents=True, exist_ok=True)
exist_ok=True подавляет ошибку при существовании папки, а parents создаёт родительские папки.

Какая функция перемещает файл в другую папку?
- shutil.copy
- shutil.move
- shutil.delete
- shutil.transfer
* Правильный ответ: shutil.move
shutil.move переносит файл или папку на новое место, сохраняя имя.

Что возвращает p.suffix для файла "report.docx"?
- "report"
- ".docx"
- "docx"
- "report.docx"
* Правильный ответ: .docx
suffix — расширение вместе с точкой.

Каким методом Bot API бот получает входящие сообщения?
- getMessages
- getUpdates
- receiveMessage
- getChat
* Правильный ответ: getUpdates
getUpdates возвращает список обновлений, включая новые сообщения.

Зачем в getUpdates передают параметр offset?
- Чтобы задать язык сообщений
- Чтобы отметить обновления прочитанными и не получать их повторно
- Чтобы ограничить длину текста
- Чтобы выбрать чат
* Правильный ответ: Чтобы отметить обновления прочитанными и не получать их повторно
offset = последний обработанный update_id + 1, и Telegram больше не пришлёт эти обновления.

Какая библиотека генерирует QR-коды?
- qrcode
- qrgen
- barcode
- qrlib
* Правильный ответ: qrcode
qrcode.make("текст") возвращает изображение QR-кода, которое сохраняется через save().

Чем thumbnail() отличается от resize() в Pillow?
- thumbnail() сохраняет пропорции и не увеличивает изображение
- thumbnail() только увеличивает изображение
- resize() сохраняет пропорции
- Ничем
* Правильный ответ: thumbnail() сохраняет пропорции и не увеличивает изображение
resize() растягивает ровно под указанные размеры, а thumbnail() вписывается в максимум.

Как создать новый Excel-файл в openpyxl?
- openpyxl.file()
- Workbook() и wb.save("file.xlsx")
- xl.create()
- sheet.make()
* Правильный ответ: Workbook() и wb.save("file.xlsx")
Workbook создаёт книгу, а save записывает её на диск.

Какой модуль отправляет электронную почту?
- emails
- mailer
- smtplib
- sendmail
* Правильный ответ: smtplib
smtplib — стандартный модуль для SMTP-отправки: подключение, starttls, login, send_message.

Какой модуль лучше всего подходит для генерации паролей?
- random
- secrets
- uuid
- string
* Правильный ответ: secrets
secrets даёт криптографически стойкие случайные значения — то, что нужно для паролей и токенов.
<!--/QUIZ-->
