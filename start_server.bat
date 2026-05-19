@echo off
echo ===================================================
echo Starting NovaSupport Agent Server...
echo ===================================================
echo.
echo Once the server starts, you can access the frontend from:
echo 1) This laptop: http://127.0.0.1:8000
echo 2) Other laptops on your Wi-Fi: http://10.228.64.45:8000
echo.
echo NOTE: If testing from another laptop, ensure Windows Defender Firewall 
echo allows incoming connections to Python/port 8000 on this laptop!
echo.
echo Keep this window open! (If you close this, the server stops)
echo.

:: Use absolute execution path to avoid PATH issues
.\venv\Scripts\python.exe -m uvicorn api:app --host 0.0.0.0 --port 8000

pause
