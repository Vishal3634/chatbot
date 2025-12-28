# Project Structure

## Directory Layout

```
RAG-CHATBOT/
├── venv/                          # Virtual environment (not in Git)
│   ├── Scripts/                   # Windows executables
│   ├── bin/                       # Mac/Linux executables
│   └── Lib/                       # Python packages
│
├── .env                           # API keys (SECRET - not in Git)
├── .gitignore                     # Git ignore rules
├── chatbot_web_app.py            # Main Streamlit application
├── documents.pkl                  # Stored document data (auto-generated)
├── faiss_index.bin               # Vector index (auto-generated)
│
├── GITHUB_PUSH_GUIDE.md          # GitHub instructions
├── LICENSE                        # MIT License
├── PROJECT_STRUCTURE.md          # This file
├── QUICK_REFERENCE.md            # Quick commands
├── README.md                      # Main documentation
├── requirements.txt               # Python dependencies
│
├── run_chatbot.bat               # Windows run script
├── run_chatbot.sh                # Mac/Linux run script
├── SETUP_GUIDE_VS_CODE.md        # VS Code setup guide
├── setup.bat                      # Windows setup script
└── setup.sh                       # Mac/Linux setup script
```

## File Descriptions

### Core Files

- **chatbot_web_app.py**: Main application with Streamlit UI
- **requirements.txt**: All Python package dependencies
- **.env**: Environment variables (API keys)

### Setup Scripts

- **setup.bat** / **setup.sh**: Automated setup (creates venv, installs packages)
- **run_chatbot.bat** / **run_chatbot.sh**: Quick start scripts

### Documentation

- **README.md**: Project overview and quick start
- **SETUP_GUIDE_VS_CODE.md**: Complete VS Code setup
- **GITHUB_PUSH_GUIDE.md**: Git and GitHub workflow
- **PROJECT_STRUCTURE.md**: This file
- **QUICK_REFERENCE.md**: Common commands reference

### Auto-Generated Files

- **documents.pkl**: Serialized document store
- **faiss_index.bin**: Vector similarity index
- **venv/**: Python virtual environment

### Configuration Files

- **.gitignore**: Files excluded from Git
- **LICENSE**: MIT License text

## Technologies Used

### Backend
- **Python 3.8+**: Core language
- **Streamlit**: Web framework
- **Google Generative AI**: AI model (Gemini)
- **Pinecone**: Vector database

### Document Processing
- **PyPDF2**: PDF reading
- **python-docx**: Word document reading
- **Pillow**: Image processing
- **pytesseract**: OCR for images

### Utilities
- **python-dotenv**: Environment variable management

## Data Flow

1. User uploads document → File reader extracts text
2. Text is chunked → Chunks are embedded
3. Embeddings stored in Pinecone
4. User asks question → Question is embedded
5. Similar chunks retrieved from Pinecone
6. Context + question sent to Gemini
7. AI response displayed to user

## Environment Variables

Required in `.env` file:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

## Ignored Files

Files in `.gitignore` (not pushed to GitHub):
- `.env` - Contains secrets
- `venv/` - Large, environment-specific
- `__pycache__/` - Python cache
- `documents.pkl` - User-generated data
- `faiss_index.bin` - User-generated data
- `.vscode/` - IDE settings