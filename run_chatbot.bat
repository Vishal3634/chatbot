@echo off
echo Starting RAG Chatbot...
echo.

if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
streamlit run chatbot_web_app.py