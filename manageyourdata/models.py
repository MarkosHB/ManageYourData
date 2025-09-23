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

    return None

def get_frontend_info(model: str) -> dict:
    """Factory function to get LLM's Streamlit button data.

    Args:
        model (str): The LLM provider.

    Returns:
        dict: Configuration parameters.

    Raises:
        ValueError: Export format not supported.
    """

    if model == constants.MODEL_PROVIDERS[0]: # "Ollama"
        config = {
            "label": "Preguntar mediante Ollama",
            "help": "Asegúrate de tener Ollama instalado y un modelo descargado.",
            "icon": "💬",
        }

    elif model == constants.MODEL_PROVIDERS[1]: # "Google"
        config = {
            "label": "Preguntar mediante la API de Google",
            "help": "Recuerda haber configurado tu clave de la API",
            "icon": "🌐",
        }

    else:
        raise ValueError(f"Unsupported LLM provider. Supported providers: {constants.MODEL_PROVIDERS}")
    
    return config
