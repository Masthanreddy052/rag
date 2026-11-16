import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DATA_DIR = os.getenv("DATA_DIR", "data/documents")
CHROMA_DIR = os.getenv("CHROMA_DIR", "vectorstore/chroma_db")
