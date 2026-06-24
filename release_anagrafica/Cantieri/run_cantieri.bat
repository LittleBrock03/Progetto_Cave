@echo off
setlocal
cd /d "%~dp0"

if not exist "logs" mkdir "logs"
set "PROGETTO_CAVE_EXPORT_DIR=%~dp0..\Anagrafica ICR"
if not exist "%PROGETTO_CAVE_EXPORT_DIR%" mkdir "%PROGETTO_CAVE_EXPORT_DIR%"

set LOG_FILE=logs\cantieri_%DATE:~-4%%DATE:~3,2%%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%.log
set LOG_FILE=%LOG_FILE: =0%

echo Avvio cantieri: %DATE% %TIME% > "%LOG_FILE%"
"%~dp0ProgettoCaveReport.exe" --config "%~dp0config\cantieri_config.json" --no-open >> "%LOG_FILE%" 2>&1
set EXIT_CODE=%ERRORLEVEL%
echo Fine cantieri: %DATE% %TIME% >> "%LOG_FILE%"
echo Codice uscita: %EXIT_CODE% >> "%LOG_FILE%"

exit /b %EXIT_CODE%
