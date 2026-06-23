@echo off
setlocal

cd /d "%~dp0"

if not exist "logs" mkdir "logs"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%I
set LOG_FILE=%~dp0logs\report_%TS%.log

echo Avvio report: %DATE% %TIME% > "%LOG_FILE%"
echo Cartella: %~dp0 >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

"%~dp0ProgettoCaveReport.exe" --source rete --months 3 --no-open %* >> "%LOG_FILE%" 2>&1
set EXIT_CODE=%ERRORLEVEL%

echo. >> "%LOG_FILE%"
echo Fine report: %DATE% %TIME% >> "%LOG_FILE%"
echo Codice uscita: %EXIT_CODE% >> "%LOG_FILE%"

exit /b %EXIT_CODE%
