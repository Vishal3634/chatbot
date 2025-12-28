# Quick Reference Guide

## Setup Commands

### Windows
```bash
# Setup
setup.bat

# Run
run_chatbot.bat
```

### Mac/Linux
```bash
# Make scripts executable
chmod +x setup.sh run_chatbot.sh

# Setup
./setup.sh

# Run
./run_chatbot.sh
```

## Manual Commands

### Create Virtual Environment
```bash
# Windows
python -m venv venv

# Mac/Linux
python3 -m venv venv
```

### Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Application
```bash
streamlit run chatbot_web_app.py
```

### Deactivate Virtual Environment
```bash
deactivate
```

## Git Commands

### Initialize Repository
```bash
git init
git add .
git commit -m "Initial commit"
```

### Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/RAG-CHATBOT.git
git branch -M main
git push -u origin main
```

### Update Code
```bash
git add .
git commit -m "Update description"
git push
```

## Troubleshooting

### Python not found
- Windows: Add Python to PATH
- Mac: Use `python3` instead of `python`

### Permission denied (Mac/Linux)
```bash
chmod +x setup.sh run_chatbot.sh
```

### Module not found
```bash
pip install -r requirements.txt
```

### Port already in use
```bash
streamlit run chatbot_web_app.py --server.port 8502
```