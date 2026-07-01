@echo off
call "%~dp0_esegui_report.bat" vettori "release_anagrafica_ICR\Vettori\config\vettori_config.json" ICR "release_anagrafica_ICR\Anagrafica ICR" "release_anagrafica_ICR\Vettori\logs"
exit /b %ERRORLEVEL%
