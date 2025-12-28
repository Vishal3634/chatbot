@echo off
echo ========================================
echo RAG Chatbot - Windows Setup Script
echo ========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo [4/4] Checking .env file...
if not exist .env (
    echo WARNING: .env file not found!
    echo Please create .env file with your API keys:
    echo GOOGLE_API_KEY=your_key
    echo PINECONE_API_KEY=your_key
    echo.
) else (
    echo ✓ .env file found
)
echo.

echo ========================================
echo Setup Complete! 🎉
echo ========================================
echo.
echo Next steps:
echo 1. Make sure .env file contains your API keys
echo 2. Run: run_chatbot.bat
echo.
pause