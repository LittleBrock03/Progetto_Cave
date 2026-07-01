@echo off
call "%~dp0_esegui_report.bat" articoli "release_anagrafica_ICR\Articoli\config\articoli_config.json" ICR "release_anagrafica_ICR\Anagrafica ICR" "release_anagrafica_ICR\Articoli\logs"
exit /b %ERRORLEVEL%
