# RAG Chatbot – Open-source embeddings

A modular Retrieval-Augmented Generation starter project using:

- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (open source, runs locally)
- **Vector store:** ChromaDB (persistent local storage)
- **Chat LLM:** Groq API (requires an API key)
- **UI:** Streamlit
- **Document types:** PDF and TXT

## 1. Create and activate a virtual environment

### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux
```bash
python -m venv .venv
source .venv/bin/activate
```

## 2. Install packages

```bash
pip install -r requirements.txt
```

## 3. Configure environment variables

Copy `.env.example` to `.env`, then add your Groq API key:

```env
GROQ_API_KEY=your_actual_key
```

The embedding model is open source and runs locally. On first use, Hugging Face downloads it and caches it on your machine. No embedding API key is required.

## 4. Add documents

Put PDF or TXT files inside:

```text
data/documents/
```

A small sample text file is included in that folder.

## 5. Build the vector database

```bash
python ingest.py
```

This loads files, splits them into chunks, creates embeddings locally, and stores them in Chroma.

Run ingestion again after adding or changing documents. This starter recreates the Chroma collection when ingesting; back up your vector store if needed.

## 6. Start the Streamlit app

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Project structure

```text
rag_project/
├── data/documents/              # Source PDF and TXT files
├── vectorstore/chroma_db/       # Persisted Chroma database
├── embeddings/embedding_model.py
├── llm/llm_model.py
├── retriever/retrieval.py
├── prompts/templates.py
├── vectorstore/chroma_db.py
├── config.py
├── ingest.py                    # Offline document ingestion
├── rag_pipeline.py              # Retrieval + prompt + LLM
├── app.py                       # Streamlit interface
├── .env.example
├── .gitignore
└── requirements.txt
```

## How a question is answered

1. Streamlit receives the question.
2. The retriever embeds the question using the same Hugging Face embedding model.
3. Chroma finds the most similar stored chunks.
4. The prompt combines the retrieved chunks with the question.
5. Groq's chat model generates an answer grounded in that context.
6. Streamlit displays the answer and retrieved source chunks.

## Notes

- `all-MiniLM-L6-v2` produces 384-dimensional embeddings.
- Keep the same embedding model and settings for ingestion and querying.
- The LLM is accessed through Groq; only the embedding model is local/open source in this starter.
- Do not commit `.env` or API keys to source control.
- This is a learning starter, not a production deployment. Add authentication, upload validation, document deletion/update handling, and stronger evaluation before production use.
