REM ...existing code...
@echo off
setlocal

REM log file
set "LOG=C:\logs\app_kill.log"
if not exist "C:\logs" mkdir "C:\logs"

echo [%date% %time%] ===== Kill script start ===== >> "%LOG%"

REM kill main app by image name
taskkill /IM flask_cms_app.exe /F >> "%LOG%" 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [%time%] flask_cms_app.exe terminated >> "%LOG%"
) else (
    echo [%time%] flask_cms_app.exe not running or failed to terminate >> "%LOG%"
)

REM kill THS-related processes by window title (e.g. "网上股票交易系统" / "同花顺")
powershell -NoProfile -Command ^
"$patterns = '网上股票交易系统','同花顺';foreach($p in Get-Process){foreach($pat in $patterns){if($p.MainWindowTitle -and $p.MainWindowTitle.Contains($pat)){Write-Output((\"Stopped PID:{0} Name:{1} Title:{2}\" -f $p.Id,$p.ProcessName,$p.MainWindowTitle));Stop-Process -Id $p.Id -Force}}}" >> "%LOG%" 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [%time%] THS-related processes termination attempted, see log for details >> "%LOG%"
) else (
    echo [%time%] Attempt to terminate THS-related processes returned non-zero exit code >> "%LOG%"
)

echo [%date% %time%] ===== Kill script end ===== >> "%LOG%"
endlocal