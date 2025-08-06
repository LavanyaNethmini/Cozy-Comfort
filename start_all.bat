@echo off
title Cozy Comfort System Launcher

REM --- Use Python launcher instead of 'python' ---
set PYTHON=py

REM --- Path to Ngrok executable ---
set NGROK_PATH=C:\ngrok\ngrok.exe  REM <-- Change if Ngrok is in a different folder

echo Starting Cozy Comfort system...
echo.

REM --- Start Flask Services ---
start cmd /k "%PYTHON% auth_service.py"
start cmd /k "%PYTHON% manufacturer_service.py"
start cmd /k "%PYTHON% distributor_service.py"
start cmd /k "%PYTHON% seller_service.py"
start cmd /k "%PYTHON% notification_service.py"

REM --- Wait a bit to let Flask start ---
timeout /t 5 >nul

REM --- Start Ngrok Tunnels ---
start cmd /k "%NGROK_PATH% http 5000"
start cmd /k "%NGROK_PATH% http 5001"
start cmd /k "%NGROK_PATH% http 5002"
start cmd /k "%NGROK_PATH% http 5003"
start cmd /k "%NGROK_PATH% http 5004"

echo.
echo All Flask services and Ngrok tunnels started.
echo Copy the Ngrok public URLs into your config.js file.
echo.
pause
