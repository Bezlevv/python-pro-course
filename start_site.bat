@echo off
rem ============================================
rem  PythonPro - double-click launcher
rem  Runs the installer/launcher PowerShell script
rem ============================================
chcp 65001 >nul
cd /d %~dp0
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start_site.ps1"
