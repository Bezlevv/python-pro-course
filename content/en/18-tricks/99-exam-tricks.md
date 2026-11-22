---
title: Exam: Cool Tricks
summary: Test your automation knowledge: pathlib/shutil, Telegram Bot API, QR codes and Pillow, openpyxl/python-docx, monitoring with requests/smtplib, secrets-based generators.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
Which pathlib method creates a folder and doesn't fail if it already exists?
- mkdir()
- mkdir(parents=True, exist_ok=True)
- create()
- newdir()
* Correct answer: mkdir(parents=True, exist_ok=True)
exist_ok=True suppresses the error when the folder exists, and parents creates parent folders.

Which function moves a file to another folder?
- shutil.copy
- shutil.move
- shutil.delete
- shutil.transfer
* Correct answer: shutil.move
shutil.move moves a file or folder to a new location, keeping its name.

What does p.suffix return for the file "report.docx"?
- "report"
- ".docx"
- "docx"
- "report.docx"
* Correct answer: .docx
suffix is the extension together with the dot.

Which Bot API method does a bot use to get incoming messages?
- getMessages
- getUpdates
- receiveMessage
- getChat
* Correct answer: getUpdates
getUpdates returns a list of updates, including new messages.

Why pass the offset parameter to getUpdates?
- To set the message language
- To mark updates as read and avoid receiving them again
- To limit the text length
- To select a chat
* Correct answer: To mark updates as read and avoid receiving them again
offset = last processed update_id + 1, and Telegram won't send those updates again.

Which library generates QR codes?
- qrcode
- qrgen
- barcode
- qrlib
* Correct answer: qrcode
qrcode.make("text") returns a QR code image, saved with save().

How is thumbnail() different from resize() in Pillow?
- thumbnail() preserves proportions and doesn't enlarge the image
- thumbnail() only enlarges the image
- resize() preserves proportions
- It isn't
* Correct answer: thumbnail() preserves proportions and doesn't enlarge the image
resize() stretches exactly to the given size, while thumbnail() fits within a maximum.

How do you create a new Excel file in openpyxl?
- openpyxl.file()
- Workbook() and wb.save("file.xlsx")
- xl.create()
- sheet.make()
* Correct answer: Workbook() and wb.save("file.xlsx")
Workbook creates the workbook, and save writes it to disk.

Which module sends email?
- emails
- mailer
- smtplib
- sendmail
* Correct answer: smtplib
smtplib is the standard module for SMTP sending: connection, starttls, login, send_message.

Which module is best for generating passwords?
- random
- secrets
- uuid
- string
* Correct answer: secrets
secrets gives cryptographically strong random values — exactly what passwords and tokens need.
<!--/QUIZ-->
