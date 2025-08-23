@echo off
:: ==============================================
:: Auto code fix script template
:: ==============================================

:: 1. Set correct code page
chcp 936 >nul

:: 2. Set console font (optional)
reg add "HKCU\Console" /v "FaceName" /t REG_SZ /d "SimSun" /f
reg add "HKCU\Console" /v "FontFamily" /t REG_DWORD /d 0 /f

:: 3. Check system locale
for /f "tokens=2*" %%A in ('reg query "HKCU\Control Panel\International" /v Locale') do (
    set "SYSTEM_LOCALE=%%B"
)
if not "%SYSTEM_LOCALE%"=="00000804" (
    echo [Warning] System locale may not be Simplified Chinese
    echo Current locale code: %SYSTEM_LOCALE%
)

:: 4. Set working directory
cd /d D:\software\

:: 5. Main program starts
echo Starting program...
echo Status check >> "%TEMP%\app_log.txt"

:: 6. Start your actual program
start "" "D:\software\flask_cms_app.exe"

:: ==============================================
:: Script ends
:: ==============================================