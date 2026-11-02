# ============================================================
#  PythonПро - запуск одним двойным кликом
#  Устанавливает зависимости, готовит базу, запускает сервер
#  и открывает сайт в браузере автоматически.
# ============================================================

param([switch]$NoBrowser)

$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$url = 'http://127.0.0.1:8000/'
$adminUrl = 'http://127.0.0.1:8000/admin/'

function Write-Step($text) {
    Write-Host ''
    Write-Host "=== $text ===" -ForegroundColor Cyan
}

# ---------- 1. Проверка Python ----------
Write-Step 'Проверка Python'
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Host 'Python не найден. Установите его командой:' -ForegroundColor Yellow
    Write-Host '  winget install Python.Python.3.13'
    Write-Host 'Затем перезапустите терминал и повторите запуск.' -ForegroundColor Yellow
    Read-Host 'Нажмите Enter для выхода'
    exit 1
}
python --version | ForEach-Object { Write-Host $_ -ForegroundColor DarkGray }

# ---------- 2. Установка зависимостей ----------
Write-Step 'Установка зависимостей (pip install -r requirements.txt)'
python -m pip install --disable-pip-version-check -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Ошибка установки зависимостей.' -ForegroundColor Red
    Read-Host 'Нажмите Enter для выхода'
    exit 1
}

# ---------- 3. Подготовка базы данных ----------
Write-Step 'Подготовка базы данных (миграции)'
python manage.py migrate --skip-checks
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Ошибка применения миграций.' -ForegroundColor Red
    Read-Host 'Нажмите Enter для выхода'
    exit 1
}

Write-Step 'Загрузка контента курса'
python manage.py load_content
python manage.py seed_achievements

# Команда ensure_admin есть не во всех версиях - запускаем, если доступна
if (python manage.py help | Select-String -Quiet 'ensure_admin') {
    python manage.py ensure_admin
}

# ---------- 4. Запуск сервера ----------
Write-Step 'Запуск сервера'
$p = $null
$listener = $null
try {
    $listener = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction Stop | Select-Object -First 1
} catch { }

if ($listener) {
    Write-Host 'Сервер уже запущен на порту 8000.' -ForegroundColor Yellow
} else {
    $log = Join-Path $PSScriptRoot 'server.log'
    $p = Start-Process python `
        -ArgumentList @('manage.py', 'runserver', '127.0.0.1:8000', '--noreload') `
        -RedirectStandardOutput $log `
        -RedirectStandardError "$log.err" `
        -WindowStyle Hidden `
        -PassThru
    Write-Host "Сервер запущен (PID $($p.Id)). Ждём готовности..." -ForegroundColor DarkGray
}

# ---------- 5. Ожидание ответа сайта ----------
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 2
    try {
        $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
        if ($r.StatusCode -eq 200) { $ready = $true; break }
    } catch { }
}

if (-not $ready) {
    Write-Host 'Сервер не ответил. Посмотрите лог: server.log / server.log.err' -ForegroundColor Red
    if (Test-Path 'server.log.err') { Get-Content 'server.log.err' -Tail 20 }
    Read-Host 'Нажмите Enter для выхода'
    exit 1
}

# ---------- 6. Открытие сайта в браузере ----------
if (-not $NoBrowser) {
    Start-Process $url
}

Write-Host ''
Write-Host '======================================================' -ForegroundColor Green
Write-Host '  Курс готов!' -ForegroundColor Green
Write-Host "  Сайт:     $url" -ForegroundColor Green
Write-Host "  Админка:  $adminUrl" -ForegroundColor Green
Write-Host '  Логин:    v.bezlepkin' -ForegroundColor DarkCyan
Write-Host '======================================================' -ForegroundColor Green
Write-Host ''

# ---------- 7. Ожидание пользователя, возможность остановки ----------
while ($true) {
    if ($p) {
        $k = Read-Host 'Нажмите [Q] чтобы остановить сервер и выйти'
        if ($k -match '^[qQ]') {
            Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
            Write-Host 'Сервер остановлен. До свидания!' -ForegroundColor DarkGray
            exit 0
        }
    } else {
        Read-Host 'Нажмите Enter для выхода'
        exit 0
    }
}
