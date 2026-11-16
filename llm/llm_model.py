from langchain_groq import ChatGroq
from config import GROQ_API_KEY, LLM_MODEL

def get_llm():
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        raise ValueError(
            "GROQ_API_KEY is missing. Add your key to the .env file."
        )
    return ChatGroq(
        model=LLM_MODEL,
        temperature=0,
        api_key=GROQ_API_KEY,
    )
