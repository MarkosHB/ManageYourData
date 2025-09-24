import streamlit as st
from manageyourdata.utils import constants
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI


def create_llm_agent(provider: str, model_selected: str, api_key: str = None):
    """Create a LangChain LLM agent based on the selected provider.

    Args:
        provider (str): The LLM provider.

    Returns:
        llm: The initialized LLM instance.

    Raises:
        ValueError: Export format not supported.
    """
    
    llm = None

    if provider == constants.MODEL_PROVIDERS[0]:  # "Ollama"
        try:
            llm = ChatOllama(model=model_selected)
        except Exception as e:
            st.error(f"Error initializing Ollama: {e}")

    elif provider == constants.MODEL_PROVIDERS[1]:  # "Google"
        try:
            llm = ChatGoogleGenerativeAI(model=model_selected, google_api_key=api_key)
        except Exception as e:
            st.error(f"Error initializing Google API: {e}")
        
    else:
        raise ValueError(f"Unsupported LLM provider. Supported providers: {constants.MODEL_PROVIDERS}")

    return llm
