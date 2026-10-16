@echo off
rem FreeMium JayRain audio node launcher (Windows)
rem First run: asks for a node password and writes it into application.yml

where java >nul 2>nul
if errorlevel 1 (
  echo.
  echo  Java 17 or newer is required but was not found.
  echo  Download it here: https://adoptium.net
  echo  Install it, then double-click this file again.
  echo.
  pause
  exit /b 1
)

findstr /C:"__NODE_PASSWORD__" application.yml >nul
if not errorlevel 1 (
  echo.
  echo  First-time setup: choose a password for your node.
  echo  You'll paste this same password into the FreeMium JayRain dashboard.
  echo.
  powershell -NoProfile -Command "$p = Read-Host 'Node password'; if ($p.Length -lt 4) { Write-Host 'Use at least 4 characters.'; exit 1 }; (Get-Content 'application.yml').Replace('__NODE_PASSWORD__', $p) | Set-Content 'application.yml'; Write-Host 'Password saved.'"
  if errorlevel 1 (
    pause
    exit /b 1
  )
)

echo.
echo  Starting your FreeMium JayRain audio node...
echo  Keep this window open while you want music. Close it to stop.
echo.
java -jar Lavalink.jar
pause
