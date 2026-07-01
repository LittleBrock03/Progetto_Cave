@echo off
call "%~dp0_esegui_report.bat" destinazione "release_anagrafica_CBR\Destinazione\config\destinazione_config.json" CBR "release_anagrafica_CBR\Anagrafica CBR" "release_anagrafica_CBR\Destinazione\logs"
exit /b %ERRORLEVEL%
