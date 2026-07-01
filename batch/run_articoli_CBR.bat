@echo off
call "%~dp0_esegui_report.bat" articoli "release_anagrafica_CBR\Articoli\config\articoli_config.json" CBR "release_anagrafica_CBR\Anagrafica CBR" "release_anagrafica_CBR\Articoli\logs"
exit /b %ERRORLEVEL%
