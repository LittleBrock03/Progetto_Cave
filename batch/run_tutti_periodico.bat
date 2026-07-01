@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "DESKTOP_DIR=%USERPROFILE%\Desktop"
if defined OneDriveCommercial if exist "%OneDriveCommercial%\Desktop" set "DESKTOP_DIR=%OneDriveCommercial%\Desktop"
if defined OneDrive if exist "%OneDrive%\Desktop" set "DESKTOP_DIR=%OneDrive%\Desktop"

set "NOTE_FILE=%DESKTOP_DIR%\Crea_Report_ERRORI.txt"
set "TEMP_NOTE=%TEMP%\Crea_Report_ERRORI_%RANDOM%_%RANDOM%.tmp"
set /a FAILURES=0

> "%TEMP_NOTE%" echo REPORT NON COMPLETATI
>> "%TEMP_NOTE%" echo Esecuzione: %DATE% %TIME%
>> "%TEMP_NOTE%" echo.

call "%~dp0_esegui_voce_totale.bat" "Anagrafe ICR" "run_anagrafe_ICR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Articoli ICR" "run_articoli_ICR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Cantieri ICR" "run_cantieri_ICR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Destinazione ICR" "run_destinazione_ICR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Tipo Documento ICR" "run_tipo_documento_ICR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Vettori ICR" "run_vettori_ICR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Voci di Spesa ICR" "run_voci_di_spesa_ICR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1

call "%~dp0_esegui_voce_totale.bat" "Anagrafe CBR" "run_anagrafe_CBR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Articoli CBR" "run_articoli_CBR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Cantieri CBR" "run_cantieri_CBR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Destinazione CBR" "run_destinazione_CBR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Tipo Documento CBR" "run_tipo_documento_CBR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Vettori CBR" "run_vettori_CBR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Voci di Spesa CBR" "run_voci_di_spesa_CBR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1

call "%~dp0_esegui_voce_totale.bat" "Contabilita CBR" "run_contabilita_CBR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1
call "%~dp0_esegui_voce_totale.bat" "Report Cave ICR" "run_report_cave_ICR.bat" "%TEMP_NOTE%"
if errorlevel 1 set /a FAILURES+=1

if !FAILURES! GTR 0 (
    >> "%TEMP_NOTE%" echo.
    >> "%TEMP_NOTE%" echo Totale report non completati: !FAILURES!
    copy /Y "%TEMP_NOTE%" "%NOTE_FILE%" >nul
    del /Q "%TEMP_NOTE%" >nul 2>&1
    echo.
    echo ATTENZIONE: !FAILURES! report non completati.
    echo Dettagli: "%NOTE_FILE%"
    exit /b 1
)

del /Q "%TEMP_NOTE%" >nul 2>&1
if exist "%NOTE_FILE%" del /Q "%NOTE_FILE%" >nul 2>&1
echo.
echo Tutti i report sono stati completati correttamente.
exit /b 0
