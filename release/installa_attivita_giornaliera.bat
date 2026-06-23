@echo off
setlocal

cd /d "%~dp0"

set TASK_NAME=ProgettoCaveReport
set TASK_TIME=07:30
set TASK_CMD=%~dp0run_report_periodico.bat

schtasks /Create /TN "%TASK_NAME%" /TR "\"%TASK_CMD%\"" /SC DAILY /ST %TASK_TIME% /F

if errorlevel 1 (
    echo.
    echo Creazione attivita non riuscita.
    echo Prova ad avviare questo file come amministratore.
    pause
    exit /b 1
)

echo.
echo Attivita creata: %TASK_NAME%
echo Frequenza: ogni giorno alle %TASK_TIME%
echo Comando: %TASK_CMD%
pause
