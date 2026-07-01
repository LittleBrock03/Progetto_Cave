@echo off
call "%~dp0_esegui_report.bat" vettori "release_anagrafica_CBR\Vettori\config\vettori_config.json" CBR "release_anagrafica_CBR\Anagrafica CBR" "release_anagrafica_CBR\Vettori\logs"
exit /b %ERRORLEVEL%
