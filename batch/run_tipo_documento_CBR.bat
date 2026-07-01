@echo off
call "%~dp0_esegui_report.bat" tipo_documento "release_anagrafica_CBR\Tipo_Documento\config\tipo_documento_config.json" CBR "release_anagrafica_CBR\Anagrafica CBR" "release_anagrafica_CBR\Tipo_Documento\logs"
exit /b %ERRORLEVEL%
