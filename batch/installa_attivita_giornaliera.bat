@echo off
setlocal
set "TASK_NAME=ProgettoCaveReport"
set "TASK_TIME=07:30"
set "SCRIPT_PATH=%~dp0run_report_periodico.bat"
schtasks /Create /TN "%TASK_NAME%" /TR "\"%SCRIPT_PATH%\"" /SC DAILY /ST %TASK_TIME% /F
if errorlevel 1 exit /b 1
echo Attivita pianificata creata: %TASK_NAME% alle %TASK_TIME%.
exit /b 0
