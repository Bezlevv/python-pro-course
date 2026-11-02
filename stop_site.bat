@echo off
rem ============================================
rem  PythonPro - stop the site server
rem  Kills whatever listens on port 8000
rem ============================================
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "$c = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue; if ($c) { $c | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }; Write-Host 'Server stopped.' -ForegroundColor Green } else { Write-Host 'No server on port 8000.' -ForegroundColor Yellow }; Start-Sleep -Seconds 1"
