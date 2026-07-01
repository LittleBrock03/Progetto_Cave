@echo off
call "%~dp0_esegui_report.bat" voci_di_spesa "release_anagrafica_CBR\Voci_Di_Spesa\config\voci_di_spesa_config.json" CBR "release_anagrafica_CBR\Anagrafica CBR" "release_anagrafica_CBR\Voci_Di_Spesa\logs"
exit /b %ERRORLEVEL%
