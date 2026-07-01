@echo off
setlocal

set "RELEASE_DIR=%~dp0.."
set "NOME_REPORT=%~1"
set "CONFIG_REL=%~2"
set "SOURCE=%~3"
set "EXPORT_REL=%~4"
set "LOG_REL=%~5"
set "SOURCE_ARG=%SOURCE%"
if /I "%SOURCE%"=="ICR" set "SOURCE_ARG=icr"
if /I "%SOURCE%"=="CBR" set "SOURCE_ARG=cbr"

if not exist "%RELEASE_DIR%\Crea_Report.exe" (
    echo ERRORE: eseguibile non trovato: "%RELEASE_DIR%\Crea_Report.exe".
    exit /b 2
)
if not exist "%RELEASE_DIR%\%CONFIG_REL%" (
    echo ERRORE: config non trovata: "%RELEASE_DIR%\%CONFIG_REL%".
    exit /b 2
)

if not exist "%RELEASE_DIR%\%LOG_REL%" mkdir "%RELEASE_DIR%\%LOG_REL%"
if not exist "%RELEASE_DIR%\%EXPORT_REL%" mkdir "%RELEASE_DIR%\%EXPORT_REL%"

set "PROGETTO_CAVE_DBF_DIR=\\172.16.2.13\arca\ditte\%SOURCE%"
set "PROGETTO_CAVE_EXPORT_DIR=%RELEASE_DIR%\%EXPORT_REL%"
set "TIMESTAMP=%DATE:~-4%%DATE:~3,2%%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"
set "LOG_FILE=%RELEASE_DIR%\%LOG_REL%\%NOME_REPORT%_%TIMESTAMP%.log"

echo Avvio %NOME_REPORT% %SOURCE%: %DATE% %TIME% > "%LOG_FILE%"
echo Config: %RELEASE_DIR%\%CONFIG_REL% >> "%LOG_FILE%"
echo Sorgente DBF: %PROGETTO_CAVE_DBF_DIR% >> "%LOG_FILE%"
echo Destinazione: %PROGETTO_CAVE_EXPORT_DIR% >> "%LOG_FILE%"

"%RELEASE_DIR%\Crea_Report.exe" --config "%RELEASE_DIR%\%CONFIG_REL%" --source "%SOURCE_ARG%" --no-open %~6 %~7 %~8 %~9 >> "%LOG_FILE%" 2>&1
set "EXIT_CODE=%ERRORLEVEL%"

echo Fine %NOME_REPORT% %SOURCE%: %DATE% %TIME% >> "%LOG_FILE%"
echo Codice uscita: %EXIT_CODE% >> "%LOG_FILE%"
if not "%EXIT_CODE%"=="0" echo ERRORE: controllare "%LOG_FILE%".

exit /b %EXIT_CODE%
