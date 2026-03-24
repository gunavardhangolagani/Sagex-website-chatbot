# utils/processing.py
from langchain_chroma import Chroma
from langchain_fireworks import FireworksEmbeddings

import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()

def fn_get_llm():
    return ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.2
    )

_vector_store = None
def fn_get_chroma_client(force_new=False):
    """
    Initialize or return ChromaDB instance with Fireworks embeddings.

    Returns:
        Chroma: Vector store instance
    """
    global _vector_store

    if _vector_store is None or force_new :
        embedding_function = FireworksEmbeddings(
            model="nomic-ai/nomic-embed-text-v1.5"
        )

        _vector_store = Chroma(
            collection_name="website_data",
            embedding_function=embedding_function,
            persist_directory="data/chroma"
        )

    return _vector_store

def fn_generate_response(prompt_messages):
    """
    Executes LLM call using Groq

    Args:
        prompt_messages (list): List of LangChain messages

    Returns:
        str: Generated response
    """

    llm = fn_get_llm()

    try:
        response = llm.invoke(prompt_messages)
        return response.content

    except Exception as e:
        raise RuntimeError(f"LLM Error: {str(e)}")


