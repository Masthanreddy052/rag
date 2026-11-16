
from pathlib import Path

from langchain_core.messages import HumanMessage, AIMessage

from embeddings.embedding_model import get_embedding_model
from vectorstore.chroma_db import load_vectorstore
from retriever.retrieval import get_retriever
from llm.llm_model import get_llm
from config import CHROMA_DIR


def build_rag_pipeline():

    if not Path(CHROMA_DIR).exists():
        raise FileNotFoundError(
            "Knowledge base not found. Run ingestion first."
        )

    embeddings = get_embedding_model()

    vectorstore = load_vectorstore(embeddings)

    retriever = get_retriever(vectorstore, k=4)

    llm = get_llm()

    def answer_question(question, chat_history=None):

        chat_history = chat_history or []

        # Retrieve relevant documents
        docs = retriever.invoke(question)

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        # Convert stored history into LangChain messages
        history_messages = []

        for message in chat_history:
            if message["role"] == "user":
                history_messages.append(
                    HumanMessage(content=message["content"])
                )
            elif message["role"] == "assistant":
                history_messages.append(
                    AIMessage(content=message["content"])
                )

        # Construct prompt
        messages = [
            (
                "system",
                """
                You are a helpful RAG assistant.

                Answer using the provided document context.
                Use previous conversation history to understand
                follow-up questions.

                If the answer is unavailable in the documents,
                clearly say that you do not have enough information.

                Do not invent facts.

                Context:
                {context}
                """
            )
        ]

        messages.extend(history_messages)

        messages.append(
            (
                "human",
                "Question: {question}"
            )
        )

        from langchain_core.prompts import ChatPromptTemplate

        prompt = ChatPromptTemplate.from_messages(messages)

        formatted_messages = prompt.format_messages(
            context=context,
            question=question
        )

        response = llm.invoke(formatted_messages)

        return response.content, docs

    return answer_question
