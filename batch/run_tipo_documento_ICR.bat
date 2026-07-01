@echo off
call "%~dp0_esegui_report.bat" tipo_documento "release_anagrafica_ICR\Tipo_Documento\config\tipo_documento_config.json" ICR "release_anagrafica_ICR\Anagrafica ICR" "release_anagrafica_ICR\Tipo_Documento\logs"
exit /b %ERRORLEVEL%
