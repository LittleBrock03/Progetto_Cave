@echo off
call "%~dp0_esegui_report.bat" cantieri "release_anagrafica_ICR\Cantieri\config\cantieri_config.json" ICR "release_anagrafica_ICR\Anagrafica ICR" "release_anagrafica_ICR\Cantieri\logs"
exit /b %ERRORLEVEL%
