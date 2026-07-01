@echo off
setlocal
call "%~dp0run_anagrafe_ICR.bat" || exit /b %ERRORLEVEL%
call "%~dp0run_articoli_ICR.bat" || exit /b %ERRORLEVEL%
call "%~dp0run_cantieri_ICR.bat" || exit /b %ERRORLEVEL%
call "%~dp0run_destinazione_ICR.bat" || exit /b %ERRORLEVEL%
call "%~dp0run_tipo_documento_ICR.bat" || exit /b %ERRORLEVEL%
call "%~dp0run_vettori_ICR.bat" || exit /b %ERRORLEVEL%
call "%~dp0run_voci_di_spesa_ICR.bat" || exit /b %ERRORLEVEL%
echo Tutti gli export anagrafici ICR sono stati completati.
exit /b 0
