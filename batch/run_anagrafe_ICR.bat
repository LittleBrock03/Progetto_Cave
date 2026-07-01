@echo off
call "%~dp0_esegui_report.bat" anagrafe "release_anagrafica_ICR\Anagrafe\config\anagrafe_config.json" ICR "release_anagrafica_ICR\Anagrafica ICR" "release_anagrafica_ICR\Anagrafe\logs"
exit /b %ERRORLEVEL%
