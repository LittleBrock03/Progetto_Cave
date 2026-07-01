@echo off
call "%~dp0_esegui_report.bat" cantieri "release_anagrafica_CBR\Cantieri\config\cantieri_config.json" CBR "release_anagrafica_CBR\Anagrafica CBR" "release_anagrafica_CBR\Cantieri\logs"
exit /b %ERRORLEVEL%
