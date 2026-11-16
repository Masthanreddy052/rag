from langchain_chroma import Chroma
from config import CHROMA_DIR

def create_vectorstore(documents, embeddings):
    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name="rag_documents",
    )

def load_vectorstore(embeddings):
    return Chroma(
        collection_name="rag_documents",
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )
