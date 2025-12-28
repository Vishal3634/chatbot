#!/bin/bash

echo "Starting RAG Chatbot..."
echo ""

if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

source venv/bin/activate
streamlit run chatbot_web_app.py