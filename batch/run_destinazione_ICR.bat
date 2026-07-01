@echo off
call "%~dp0_esegui_report.bat" destinazione "release_anagrafica_ICR\Destinazione\config\destinazione_config.json" ICR "release_anagrafica_ICR\Anagrafica ICR" "release_anagrafica_ICR\Destinazione\logs"
exit /b %ERRORLEVEL%
