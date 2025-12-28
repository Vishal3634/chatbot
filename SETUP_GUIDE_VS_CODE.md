# 🚀 Complete Setup Guide for Visual Studio Code

## 📋 What You'll Need

Before starting, make sure you have:
- A Windows/Mac/Linux computer
- Internet connection
- Administrator access (for installations)

---

## STEP 1: Install Python 🐍

### Windows:
1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.11.x" (or latest version)
3. **IMPORTANT**: Check ✅ "Add Python to PATH" during installation
4. Click "Install Now"
5. Wait for installation to complete

### Mac:
1. Open Terminal
2. Install Homebrew (if not installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```bash
   brew install python
   ```

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### ✅ Verify Installation:
Open Command Prompt/Terminal and type:
```bash
python --version
```
You should see: `Python 3.11.x` or similar

---

## STEP 2: Install Visual Studio Code 💻

### Windows/Mac/Linux:
1. Go to https://code.visualstudio.com/
2. Click "Download" for your operating system
3. Run the installer
4. Follow installation wizard
5. Launch Visual Studio Code

---

## STEP 3: Install Python Extension in VS Code 🔌

1. Open Visual Studio Code
2. Click on Extensions icon (or press `Ctrl+Shift+X` / `Cmd+Shift+X`)
3. Search for "Python"
4. Install the official "Python" extension by Microsoft
5. Wait for installation to complete

---

## STEP 4: Install Tesseract OCR 📸

### Windows:
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Click on "tesseract-ocr-w64-setup-5.3.x.exe" (latest version)
3. Run the installer
4. **Remember the installation path** (usually `C:\Program Files\Tesseract-OCR`)
5. Add to PATH:
   - Right-click "This PC" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find "Path"
   - Click "Edit" → "New"
   - Add: `C:\Program Files\Tesseract-OCR`
   - Click OK on all windows

### Mac:
```bash
brew install tesseract
```

### Linux:
```bash
sudo apt-get install tesseract-ocr
```

### ✅ Verify Installation:
```bash
tesseract --version
```
You should see version information

---

## STEP 5: Create Project Folder 📁

### Windows:
1. Open File Explorer
2. Navigate to a location (e.g., `C:\Users\YourName\Documents`)
3. Create a new folder called `RAG-Chatbot`
4. Right-click the folder → "Open with Code"

### Mac/Linux:
1. Open Terminal
2. Create folder:
   ```bash
   cd ~/Documents
   mkdir RAG-Chatbot
   cd RAG-Chatbot
   code .
   ```

Your Visual Studio Code should now open with this folder

---

## STEP 6: Create Project Files 📝

In VS Code, create these 3 files:

### File 1: chatbot_web_app.py
1. Click "New File" icon or press `Ctrl+N` / `Cmd+N`
2. Save as: `chatbot_web_app.py`
3. Copy and paste the code from the `chatbot_web_app.py` file I provided
4. **IMPORTANT**: Replace the API key:
   ```python
   API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
   ```

### File 2: requirements.txt
1. Click "New File"
2. Save as: `requirements.txt`
3. Copy and paste:
   ```
   streamlit>=1.28.0
   google-generativeai>=0.3.0
   numpy>=1.24.0
   faiss-cpu>=1.7.4
   PyPDF2>=3.0.0
   python-docx>=1.0.0
   Pillow>=10.0.0
   pytesseract>=0.3.10
   ```

### File 3: README.md (Optional)
1. Click "New File"
2. Save as: `README.md`
3. Copy the README content I provided

Your folder should now have:
```
RAG-Chatbot/
├── chatbot_web_app.py
├── requirements.txt
└── README.md
```

---

## STEP 7: Open Terminal in VS Code 💻

1. In VS Code, go to menu: `Terminal` → `New Terminal`
2. Or press: `Ctrl+` ` (backtick) or `Cmd+` ` on Mac

You should see a terminal panel at the bottom

---

## STEP 8: Create Virtual Environment 🔒

### Why? 
To keep project dependencies isolated and organized.

### Windows:
```bash
python -m venv venv
```

### Mac/Linux:
```bash
python3 -m venv venv
```

Wait for it to complete (~30 seconds)

---

## STEP 9: Activate Virtual Environment ⚡

### Windows (Command Prompt):
```bash
venv\Scripts\activate
```

### Windows (PowerShell):
```bash
venv\Scripts\Activate.ps1
```

### Mac/Linux:
```bash
source venv/bin/activate
```

### ✅ Success Check:
You should see `(venv)` at the start of your terminal line:
```
(venv) C:\Users\YourName\Documents\RAG-Chatbot>
```

---

## STEP 10: Install Dependencies 📦

With virtual environment activated, run:

```bash
pip install -r requirements.txt
```

This will take 2-5 minutes. You'll see installation progress for each package.

### ✅ Verify Installation:
```bash
pip list
```
You should see all the packages listed

---

## STEP 11: Get Google API Key 🔑

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (it looks like: `AIzaSy...`)
5. Open `chatbot_web_app.py` in VS Code
6. Find line: `API_KEY = "AIzaSyBl3eq4KHMm24w9RvCCEpOdh0PnxVSjKAE"`
7. Replace with your key: `API_KEY = "YOUR_KEY_HERE"`
8. Save the file (`Ctrl+S` / `Cmd+S`)

---

## STEP 12: Run the Application! 🚀

In the VS Code terminal (with venv activated):

```bash
streamlit run chatbot_web_app.py
```

### What Happens:
1. Terminal shows: "You can now view your Streamlit app in your browser"
2. Browser automatically opens to: `http://localhost:8501`
3. You see your chatbot interface! 🎉

---

## STEP 13: Using Your Chatbot 💬

### Upload Files:
1. Look for the sidebar on the left
2. See "Upload documents" section
3. Click "Browse files" or drag & drop files
4. Click "📤 Process Uploaded Files"
5. Wait for success message

### Paste Screenshots:
1. Take a screenshot:
   - Windows: `Win+Shift+S`
   - Mac: `Cmd+Shift+4`
2. Go to upload area
3. Press `Ctrl+V` / `Cmd+V`
4. File appears!
5. Process it

### Chat:
1. Scroll to chat area
2. Type question in input box at bottom
3. Press Enter
4. Get response with mode indicator (📚 RAG or 💬 Chat)

---

## 🎯 Quick Reference Commands

### Starting Your Chatbot (Every Time):

1. Open VS Code
2. Open Terminal (`Ctrl+` `)
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Run: `streamlit run chatbot_web_app.py`

### Stopping the Chatbot:
- In terminal, press: `Ctrl+C`
- Close browser tab

---

## 🐛 Troubleshooting

### Problem: "Python is not recognized"
**Solution**: Reinstall Python and check "Add to PATH"

### Problem: "streamlit: command not found"
**Solution**: 
1. Check virtual environment is activated (see `(venv)`)
2. Run: `pip install streamlit`

### Problem: "No module named 'pytesseract'"
**Solution**: 
1. Install Tesseract OCR
2. Add to PATH
3. Restart VS Code

### Problem: "Permission denied"
**Solution** (Windows PowerShell):
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: Terminal shows errors when activating venv
**Solution** (Windows):
Try using Command Prompt instead of PowerShell:
1. Terminal → New Terminal
2. Click dropdown → "Command Prompt"

### Problem: API key error
**Solution**:
1. Verify key is correct
2. Check Google API Console for quota
3. Enable Generative AI API

### Problem: "Address already in use"
**Solution**:
Another app is using port 8501. Either:
- Close other Streamlit apps
- Or run: `streamlit run chatbot_web_app.py --server.port 8502`

---

## 📁 Project Structure After Setup

```
RAG-Chatbot/
├── venv/                    # Virtual environment (created)
├── chatbot_web_app.py       # Main application
├── requirements.txt         # Dependencies
├── README.md               # Documentation
├── faiss_index.bin         # Auto-created when you run
└── documents.pkl           # Auto-created when you run
```

---

## 💡 Pro Tips

### Tip 1: Keep Terminal Open
Don't close the terminal while using the app - it's running the server

### Tip 2: Auto-Reload
Streamlit auto-reloads when you save changes to the code

### Tip 3: Multiple Files
You can upload multiple files at once - just select them all

### Tip 4: Clear Data
To reset knowledge base, delete `faiss_index.bin` and `documents.pkl`

### Tip 5: View Logs
Terminal shows all processing logs - useful for debugging

---

## 🎨 Customize Your Chatbot

### Change Colors:
1. Create folder: `.streamlit`
2. Create file: `.streamlit/config.toml`
3. Add:
   ```toml
   [theme]
   primaryColor = "#FF4B4B"
   backgroundColor = "#FFFFFF"
   secondaryBackgroundColor = "#F0F2F6"
   textColor = "#262730"
   ```

### Change Port:
```bash
streamlit run chatbot_web_app.py --server.port 8080
```

---

## 🔄 Daily Usage Workflow

### Starting Your Work Session:
```bash
# 1. Open VS Code
# 2. Open folder: RAG-Chatbot
# 3. Open terminal (Ctrl+`)
# 4. Activate venv
venv\Scripts\activate           # Windows
source venv/bin/activate        # Mac/Linux

# 5. Run app
streamlit run chatbot_web_app.py
```

### Ending Your Work Session:
```bash
# 1. Stop app (Ctrl+C in terminal)
# 2. Deactivate venv
deactivate

# 3. Close VS Code
```

---

## ✅ Final Checklist

Before asking for help, verify:

- [ ] Python installed (`python --version`)
- [ ] VS Code installed
- [ ] Python extension installed in VS Code
- [ ] Tesseract installed (`tesseract --version`)
- [ ] Virtual environment created and activated (`(venv)` visible)
- [ ] Dependencies installed (`pip list` shows packages)
- [ ] API key updated in code
- [ ] No other app using port 8501

---

## 🎉 You're All Set!

Your chatbot is ready to use. Enjoy uploading files, pasting screenshots, and chatting!

---

## 📞 Need Help?

Common issues and solutions are in the Troubleshooting section above.

Remember: Always activate your virtual environment before running the app!
