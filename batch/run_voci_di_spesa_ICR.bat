@echo off
call "%~dp0_esegui_report.bat" voci_di_spesa "release_anagrafica_ICR\Voci_Di_Spesa\config\voci_di_spesa_config.json" ICR "release_anagrafica_ICR\Anagrafica ICR" "release_anagrafica_ICR\Voci_Di_Spesa\logs"
exit /b %ERRORLEVEL%
