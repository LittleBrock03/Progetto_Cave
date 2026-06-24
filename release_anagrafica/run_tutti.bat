@echo off
setlocal
cd /d "%~dp0"

call "%~dp0Anagrafe\run_anagrafe.bat" || exit /b %ERRORLEVEL%
call "%~dp0Articoli\run_articoli.bat" || exit /b %ERRORLEVEL%
call "%~dp0Cantieri\run_cantieri.bat" || exit /b %ERRORLEVEL%
call "%~dp0Destinazione\run_destinazione.bat" || exit /b %ERRORLEVEL%
call "%~dp0Tipo_Documento\run_tipo_documento.bat" || exit /b %ERRORLEVEL%
call "%~dp0Vettori\run_vettori.bat" || exit /b %ERRORLEVEL%
call "%~dp0Voci_Di_Spesa\run_voci_di_spesa.bat" || exit /b %ERRORLEVEL%

echo Tutti gli export sono stati completati in "%~dp0Anagrafica ICR".
pause
