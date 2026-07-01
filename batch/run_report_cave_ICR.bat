@echo off
call "%~dp0_esegui_report.bat" report_cave "release_report_cave_ICR\config\report_config.json" ICR "release_report_cave_ICR\export" "release_report_cave_ICR\logs" --months 3
exit /b %ERRORLEVEL%
