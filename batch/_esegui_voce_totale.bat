@echo off
setlocal EnableExtensions

set "REPORT_NAME=%~1"
set "REPORT_BATCH=%~2"
set "TEMP_NOTE=%~3"

echo.
echo ============================================================
echo Avvio: %REPORT_NAME%
echo ============================================================

call "%~dp0%REPORT_BATCH%"
set "REPORT_EXIT=%ERRORLEVEL%"

if not "%REPORT_EXIT%"=="0" (
    >> "%TEMP_NOTE%" echo - %REPORT_NAME% ^(codice uscita %REPORT_EXIT%^)
    echo ERRORE: %REPORT_NAME%, codice %REPORT_EXIT%. Proseguo con il report successivo.
    exit /b 1
)

echo Completato: %REPORT_NAME%
exit /b 0
