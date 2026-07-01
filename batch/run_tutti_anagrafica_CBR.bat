@echo off
setlocal
call "%~dp0run_anagrafe_CBR.bat" || exit /b %ERRORLEVEL%
call "%~dp0run_articoli_CBR.bat" || exit /b %ERRORLEVEL%
call "%~dp0run_cantieri_CBR.bat" || exit /b %ERRORLEVEL%
call "%~dp0run_destinazione_CBR.bat" || exit /b %ERRORLEVEL%
call "%~dp0run_tipo_documento_CBR.bat" || exit /b %ERRORLEVEL%
call "%~dp0run_vettori_CBR.bat" || exit /b %ERRORLEVEL%
call "%~dp0run_voci_di_spesa_CBR.bat" || exit /b %ERRORLEVEL%
echo Tutti gli export anagrafici CBR sono stati completati.
exit /b 0
