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
echo Opening Enhanced Application...
start "" "enhanced_test_app.html"

echo.
echo ========================================
echo Application is now running!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend: enhanced_test_app.html (opened in browser)
echo.
echo Instructions:
echo 1. Add parts or click "Load Sample Data"
echo 2. Click "Start Scraping" to begin
echo 3. Click on any result card to see detailed information
echo.
echo To stop the backend, close the backend window.
echo.
pause
