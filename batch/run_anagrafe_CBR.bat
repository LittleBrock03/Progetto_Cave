@echo off
call "%~dp0_esegui_report.bat" anagrafe "release_anagrafica_CBR\Anagrafe\config\anagrafe_config.json" CBR "release_anagrafica_CBR\Anagrafica CBR" "release_anagrafica_CBR\Anagrafe\logs"
exit /b %ERRORLEVEL%
