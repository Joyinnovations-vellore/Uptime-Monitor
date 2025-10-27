@echo off
echo ========================================
echo Web Scraping & AI Enrichment Application
echo ========================================
echo.

echo Starting Backend Server...
start "Backend Server" cmd /k "python main.py"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Opening Application in Browser...
start "" "test_app.html"

echo.
echo ========================================
echo Application is now running!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend: test_app.html (opened in browser)
echo.
echo To stop the backend, close the backend window.
echo.
pause
