import streamlit as st
from manageyourdata.utils import constants
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI


def create_llm_agent(provider: str, api_key: str = None):
    """Create a LangChain LLM agent based on the selected provider.

    Args:
        provider (str): The LLM provider.

    Returns:
        llm: The initialized LLM instance.

    Raises:
        ValueError: Export format not supported.
    """

    if provider == constants.MODEL_PROVIDERS[0]:  # "Ollama"
        try:
            llm = ChatOllama(model="llama3.2")
            return llm
        except Exception as e:
            st.error(f"Error initializing Ollama: {e}")
            return None

    elif provider == constants.MODEL_PROVIDERS[1]:  # "Google"
        try:
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
            return llm
        except Exception as e:
            st.error(f"Error initializing Google API: {e}")
            return None
        
    else:
        raise ValueError(f"Unsupported LLM provider. Supported providers: {constants.MODEL_PROVIDERS}")
