import streamlit as st
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
from docx import Document 
from PIL import Image 
import pytesseract  
import io
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import time

# Load environment variables
load_dotenv()

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Personal Assistant Chatbot ",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: #000000; 
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
        color: #000000; 
    }
    .info-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== SETUP ==========
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("⚠️ Google API Key not found!")
    st.info("Please create a .env file with your GOOGLE_API_KEY")
    st.stop()

if not PINECONE_API_KEY:
    st.error("⚠️ Pinecone API Key not found!")
    st.info("Please add your PINECONE_API_KEY to the .env file")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,  
    "max_output_tokens": 2048,
}

@st.cache_resource
def get_model():
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction="""You are a helpful assistant with access to documents.
        When context is provided, use it to answer accurately.
        When no context is provided, answer based on general knowledge.
        Remember previous conversation details."""
    )

model = get_model()

# ========== PINECONE SETUP ==========
INDEX_NAME = "rag-chatbot"  # You can change this name
DIMENSION = 768  # Google's text-embedding-004 dimension

@st.cache_resource
def initialize_pinecone():
    """Initialize Pinecone connection and create/connect to index"""
    try:
        # Initialize Pinecone
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Check if index exists, if not create it
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        if INDEX_NAME not in existing_indexes:
            st.info(f"Creating new Pinecone index: {INDEX_NAME}")
            pc.create_index(
                name=INDEX_NAME,
                dimension=DIMENSION,
                metric="cosine",  # cosine similarity for semantic search
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"  # Change to your preferred region
                )
            )
            # Wait for index to be ready
            time.sleep(1)
        
        # Connect to index
        index = pc.Index(INDEX_NAME)
        return pc, index
    
    except Exception as e:
        st.error(f"Error initializing Pinecone: {e}")
        st.stop()

# ========== FILE READERS (Same as before) ==========

def read_pdf(file_bytes):
    """Extract text from PDF file bytes"""
    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def read_word(file_bytes):
    """Extract text from Word document bytes"""
    try:
        doc_file = io.BytesIO(file_bytes)
        doc = Document(doc_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        st.error(f"Error reading Word: {e}")
        return None

def read_image(file_bytes):
    """Extract text from image using OCR"""
    try:
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        st.error(f"Error reading image: {e}")
        st.warning("Note: Make sure Tesseract is installed on your system")
        return None

def read_text_file(file_bytes):
    """Read plain text file"""
    try:
        text = file_bytes.decode('utf-8')
        return text.strip()
    except Exception as e:
        st.error(f"Error reading text file: {e}")
        return None

def read_uploaded_file(uploaded_file):
    """Smart file reader - detects type and reads accordingly"""
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name
    ext = os.path.splitext(file_name)[1].lower()
    
    if ext == '.pdf':
        return read_pdf(file_bytes)
    elif ext in ['.docx', '.doc']:
        return read_word(file_bytes)
    elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
        return read_image(file_bytes)
    elif ext in ['.txt', '.md', '.csv']:
        return read_text_file(file_bytes)
    else:
        st.error(f"Unsupported file type: {ext}")
        st.info("Supported: .pdf, .docx, .txt, .png, .jpg, .jpeg")
        return None

# ========== CHUNKING ==========

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split large text into smaller chunks with overlap"""
    if len(text) < chunk_size:
        return [text]
    
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

# ========== EMBEDDING ==========

def get_embedding(text, task_type="retrieval_document"):
    """Convert text to embedding using Google's API"""
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type=task_type
    )
    return result['embedding']

# ========== PINECONE OPERATIONS ==========

def add_document_to_pinecone(text, index, doc_id=None, metadata=None):
    """
    Add document to Pinecone index
    
    Args:
        text: Document text to embed and store
        index: Pinecone index object
        doc_id: Unique ID for the document (auto-generated if None)
        metadata: Additional metadata to store with the vector
    """
    try:
        # Generate unique ID if not provided
        if doc_id is None:
            doc_id = f"doc_{int(time.time() * 1000)}"
        
        # Check if text is too large and needs chunking
        if len(text) > 2000:
            chunks = chunk_text(text, chunk_size=1000, overlap=200)
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id}_chunk_{i}"
                embedding = get_embedding(chunk)
                
                # Prepare metadata
                chunk_metadata = {
                    "text": chunk[:1000],  # Store first 1000 chars
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "parent_id": doc_id
                }
                
                if metadata:
                    chunk_metadata.update(metadata)
                
                # Upsert to Pinecone
                index.upsert(vectors=[(chunk_id, embedding, chunk_metadata)])
            
            return len(chunks)
        else:
            # Single document - no chunking needed
            embedding = get_embedding(text)
            
            doc_metadata = {
                "text": text[:1000],  # Store first 1000 chars
                "chunk_index": 0,
                "total_chunks": 1
            }
            
            if metadata:
                doc_metadata.update(metadata)
            
            # Upsert to Pinecone
            index.upsert(vectors=[(doc_id, embedding, doc_metadata)])
            
            return 1
    
    except Exception as e:
        st.error(f"Error adding document to Pinecone: {e}")
        return 0

def search_pinecone(question, index, top_k=3):
    """
    Search Pinecone for relevant documents
    
    Args:
        question: User's question
        index: Pinecone index object
        top_k: Number of results to return
    
    Returns:
        relevant_docs: List of relevant document texts
        scores: Similarity scores
        matches: Full match objects from Pinecone
    """
    try:
        # Get question embedding
        question_embedding = get_embedding(question, task_type="retrieval_query")
        
        # Search Pinecone
        results = index.query(
            vector=question_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        # Extract results
        relevant_docs = []
        scores = []
        
        for match in results['matches']:
            relevant_docs.append(match['metadata'].get('text', ''))
            scores.append(match['score'])
        
        return relevant_docs, scores, results['matches']
    
    except Exception as e:
        st.error(f"Error searching Pinecone: {e}")
        return [], [], []

def is_document_related(question, best_score):
    """
    Decide if question is about documents based on similarity score
    Pinecone uses cosine similarity (0-1 range, higher is better)
    """
    THRESHOLD = 0.7  # Adjust based on your needs
    return best_score > THRESHOLD

# ========== ANSWER GENERATION ==========

def ask_question(question, chat, index):
    """Answer question using RAG or chat"""
    relevant_docs, scores, matches = search_pinecone(question, index, top_k=3)
    
    # Check if we have relevant documents
    best_score = scores[0] if scores else 0
    mode = "RAG" if is_document_related(question, best_score) else "CHAT"
    
    if mode == "RAG" and relevant_docs:
        context = "\n".join(relevant_docs)
        prompt = f"""Context from documents:
{context}

Question: {question}

Answer using the context above."""
    else:
        prompt = question
    
    response = chat.send_message(prompt)
    
    if response.candidates:
        return response.text, mode, relevant_docs if mode == "RAG" else []
    else:
        return "I'm sorry, I cannot answer that.", mode, []

# ========== INITIALIZE SAMPLE DATA ==========

def initialize_sample_documents(index):
    """Add sample documents to Pinecone on first run"""
    # Check if we have any vectors
    stats = index.describe_index_stats()
    
    if stats['total_vector_count'] == 0:
        st.info("Initializing knowledge base with sample documents...")
        
        sample_docs = [
            "The company was founded in 2010. We have 500 employees.",
            "We have offices in New York, London, and Tokyo. New York is our headquarters.",
            "Our CEO is Jane Smith. She has 20 years of tech experience.",
            "We offer ChatBot Pro, RecommendAI, and DataInsight products.",
            "Our revenue is $50 million with 80% growth rate.",
            "Jane Smith previously worked at Google and Microsoft.",
            "The headquarters houses our main R&D team of 200 researchers."
        ]
        
        for i, doc in enumerate(sample_docs):
            add_document_to_pinecone(
                doc, 
                index, 
                doc_id=f"sample_{i}",
                metadata={"source": "sample", "doc_num": i}
            )
        
        st.success("✅ Sample documents added!")

# ========== SESSION STATE ==========

if 'pc' not in st.session_state:
    st.session_state.pc, st.session_state.index = initialize_pinecone()
    initialize_sample_documents(st.session_state.index)

if 'chat' not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if 'messages' not in st.session_state:
    st.session_state.messages = []

# ========== MAIN UI ==========

# Header
st.markdown('<div class="main-header">🤖 Personal Assistant Chatbot</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📁 Document Management")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload documents (PDF, Word, Images, Text)",
        type=['pdf', 'docx', 'doc', 'txt', 'md', 'csv', 'png', 'jpg', 'jpeg', 'bmp', 'gif'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("📤 Process Uploaded Files", type="primary"):
            with st.spinner("Processing files..."):
                for uploaded_file in uploaded_files:
                    st.info(f"Processing: {uploaded_file.name}")
                    text = read_uploaded_file(uploaded_file)
                    
                    if text:
                        chunks_added = add_document_to_pinecone(
                            text, 
                            st.session_state.index,
                            metadata={
                                "filename": uploaded_file.name,
                                "upload_time": time.time()
                            }
                        )
                        st.success(f"✅ {uploaded_file.name} added ({chunks_added} chunks)!")
                    else:
                        st.error(f"❌ Failed to process {uploaded_file.name}")
    
    st.markdown("---")
    
    # Add text directly
    st.subheader("✍️ Add Text Directly")
    direct_text = st.text_area("Enter text to add to knowledge base:", height=100)
    
    if st.button("➕ Add Text"):
        if direct_text.strip():
            with st.spinner("Adding text..."):
                chunks_added = add_document_to_pinecone(
                    direct_text, 
                    st.session_state.index,
                    metadata={"source": "direct_input"}
                )
                st.success(f"✅ Text added ({chunks_added} chunks)!")
        else:
            st.warning("Please enter some text first")
    
    st.markdown("---")
    
    # View index stats
    st.subheader("📊 Pinecone Index Stats")
    if st.button("🔄 Refresh Stats"):
        stats = st.session_state.index.describe_index_stats()
        st.metric("Total Vectors", stats['total_vector_count'])
        st.metric("Index Dimension", stats.get('dimension', DIMENSION))
    
    st.markdown("---")
    
    # Clear chat
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()
    
    # Delete all vectors (use carefully!)
    st.markdown("---")
    st.subheader("⚠️ Danger Zone")
    if st.button("🗑️ Delete All Documents", type="secondary"):
        if st.checkbox("I understand this will delete all documents"):
            with st.spinner("Deleting all vectors..."):
                st.session_state.index.delete(delete_all=True)
                st.warning("All documents deleted!")
                st.rerun()

# Main chat area
st.subheader("💬 Chat")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', 
                   unsafe_allow_html=True)
    else:
        mode_badge = "📚 RAG" if message.get("mode") == "RAG" else "💭 Chat"
        st.markdown(f'<div class="chat-message bot-message"><strong>Bot {mode_badge}:</strong> {message["content"]}</div>', 
                   unsafe_allow_html=True)
        
        # Show relevant docs if RAG mode
        if message.get("mode") == "RAG" and message.get("relevant_docs"):
            with st.expander("📄 See relevant documents"):
                for i, doc in enumerate(message["relevant_docs"], 1):
                    st.text(f"{i}. {doc[:200]}...")

# Chat input
user_input = st.chat_input("Ask a question...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get bot response
    with st.spinner("Thinking..."):
        answer, mode, relevant_docs = ask_question(
            user_input, 
            st.session_state.chat, 
            st.session_state.index
        )
    
    # Add bot message
    st.session_state.messages.append({
        "role": "bot", 
        "content": answer, 
        "mode": mode,
        "relevant_docs": relevant_docs
    })
    
    # Rerun to update UI
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    💡 <strong>Powered by Pinecone</strong> - Scalable vector storage in the cloud!<br>
    Your documents are stored in Pinecone's managed infrastructure.
</div>
""", unsafe_allow_html=True)