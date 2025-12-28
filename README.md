# 🤖 RAG Chatbot with Pinecone

A powerful Retrieval-Augmented Generation (RAG) chatbot using Pinecone vector database and Google's Gemini AI.

## ✨ Features

- 📄 Multi-format document support (PDF, DOCX, TXT, Images)
- 🔍 Semantic search with Pinecone
- 💬 Context-aware AI responses
- 📝 Direct text input
- 🎨 Beautiful Streamlit UI

## 🚀 Quick Start

### Windows
```bash
setup.bat
run_chatbot.bat
```

### Mac/Linux
```bash
chmod +x setup.sh run_chatbot.sh
./setup.sh
./run_chatbot.sh
```

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API Key
- Pinecone API Key
- Tesseract OCR (for image processing)

## ⚙️ Manual Setup

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your API keys:
```env
GOOGLE_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
```

5. Run the application:
```bash
streamlit run chatbot_web_app.py
```

## 🔑 Get API Keys

- **Google Gemini**: https://makersuite.google.com/app/apikey
- **Pinecone**: https://www.pinecone.io/

## 📖 Documentation

- `SETUP_GUIDE_VS_CODE.md` - Complete VS Code setup guide
- `GITHUB_PUSH_GUIDE.md` - Git and GitHub instructions
- `PROJECT_STRUCTURE.md` - Project architecture
- `QUICK_REFERENCE.md` - Common commands

## 🌐 Deployment

Deploy to Streamlit Cloud:
1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Connect your repository
4. Add secrets (API keys)
5. Deploy!

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.0 Flash
- **Vector DB**: Pinecone
- **OCR**: Tesseract
- **PDF Processing**: PyPDF2
- **Word Processing**: python-docx

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.