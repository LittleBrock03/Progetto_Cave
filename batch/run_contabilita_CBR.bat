@echo off
call "%~dp0_esegui_report.bat" contabilita "release_contabilita_CBR\Contabilita\config\contabilita_config.json" CBR "release_contabilita_CBR\Contabilita CBR" "release_contabilita_CBR\Contabilita\logs"
exit /b %ERRORLEVEL%
