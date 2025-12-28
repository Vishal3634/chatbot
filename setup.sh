#!/bin/bash

echo "========================================"
echo "RAG Chatbot - Setup Script"
echo "========================================"
echo ""

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi
echo "✓ Virtual environment created"
echo ""

echo "[2/4] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

echo "[3/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

echo "[4/4] Checking .env file..."
if [ ! -f .env ]; then
    echo "WARNING: .env file not found!"
    echo "Please create .env file with your API keys:"
    echo "GOOGLE_API_KEY=your_key"
    echo "PINECONE_API_KEY=your_key"
    echo ""
else
    echo "✓ .env file found"
fi
echo ""

echo "========================================"
echo "Setup Complete! 🎉"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Make sure .env file contains your API keys"
echo "2. Run: ./run_chatbot.sh"
echo ""