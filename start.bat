@echo off
chcp 65001 >nul
cd /d %~dp0

echo === PythonПро: установка зависимостей ===
python -m pip install -r requirements.txt

echo === PythonПро: миграции базы данных ===
python manage.py migrate

echo === PythonПро: загрузка контента курса ===
python manage.py load_content

echo.
echo ============================================
echo  Готово! Открывай http://127.0.0.1:8000/
echo  Админка: http://127.0.0.1:8000/admin/
echo ============================================
echo.

python manage.py runserver
