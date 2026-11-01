# =========================================================
#  PythonПро — установка и запуск курса (Windows PowerShell)
#  Запуск:  .\setup.ps1   (в корне распакованного пакета)
# =========================================================

Set-Location -Path $PSScriptRoot

Write-Host "`n== 1. Проверка Python ==" -ForegroundColor Cyan
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Host "Python не найден. Установи его командой:"
    Write-Host "   winget install Python.Python.3.13"
    Write-Host "Затем перезапусти терминал и повтори запуск." -ForegroundColor Yellow
    exit 1
}
python --version
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "`n== 2. Обновление pip и установка зависимостей ==" -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { Write-Host "Ошибка установки зависимостей." -ForegroundColor Red; exit 1 }

Write-Host "`n== 3. Подготовка базы данных ==" -ForegroundColor Cyan
python manage.py migrate
if ($LASTEXITCODE -ne 0) { exit 1 }
python manage.py load_content
python manage.py seed_achievements
python manage.py ensure_admin

Write-Host "`n== 4. Запуск сервера ==" -ForegroundColor Cyan
$running = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -First 1
if ($running) {
    Write-Host "Сервер уже запущен на порту 8000."
} else {
    Start-Process python -ArgumentList 'manage.py','runserver','127.0.0.1:8000','--noreload' -WindowStyle Hidden
    Start-Sleep -Seconds 5
}

try {
    $r = Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/
    Write-Host "`nУспех! HTTP $($r.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Сервер не ответил. Запусти вручную: python manage.py runserver" -ForegroundColor Yellow
}

Write-Host "`n===============================" -ForegroundColor Cyan
Write-Host "  Курс:  http://127.0.0.1:8000/"  -ForegroundColor Green
Write-Host "  Админка: http://127.0.0.1:8000/admin/" -ForegroundColor Green
Write-Host "  Логин админа: v.bezlepkin" -ForegroundColor DarkCyan
Write-Host "  Пароль: Bezlevv4591" -ForegroundColor DarkCyan
Write-Host "===============================" -ForegroundColor Cyan
