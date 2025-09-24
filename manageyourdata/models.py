from manageyourdata.utils import constants
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI


def create_llm_agent(provider: str, model_selected: str, api_key: str = None):
    """Create a LangChain LLM agent based on the selected provider.

    Args:
        provider (str): The LLM provider.
        model_selected (str): The model name to be used.
        api_key (str, optional): API key for providers that require authentication.

    Returns:
        llm: The initialized LLM instance.

    Raises:
        ValueError: LLM could not be initialized.
    """

    llm = None

    # "Ollama"
    if provider == constants.MODEL_PROVIDERS[0]:
        try:
            llm = ChatOllama(model=model_selected)
        except Exception:
            raise ValueError(f"Error al iniciar Ollama. Comprueba que la información dada en la configuración sea correcta.")

    # "Google"
    elif provider == constants.MODEL_PROVIDERS[1]:  
        try:
            llm = ChatGoogleGenerativeAI(model=model_selected, google_api_key=api_key)
        except Exception as e:
            raise ValueError(f"Error al iniciar google Gemini. Comprueba que la información dada en la configuración sea correcta.")

    else:
        raise ValueError(f"Unsupported LLM provider. Supported providers: {constants.MODEL_PROVIDERS}")

    return llm


CONFIG_PROMT="""
Eres un analista de datos experto con un conocimiento profundo en el análisis y la interpretación de conjuntos de datos (datasets). 
Tu objetivo es analizar un DataFrame de pandas y extraer métricas con aspectos destacables que sean útiles para un usuario no técnico.
Debes ceñirte en todo momento a lo que el usuario te ha pedido realizar.

Algunas sugerencias para el análisis pueden ser:

**Visión general del Dataset:**
    - Proporciona un resumen conciso del dataset.
    - Describe la naturaleza de los datos.

**Métricas Clave:**
    - Descata anomalías o aspectos interesantes en las principales métricas si es conveniente.

**Aspectos Destacables y Anomalías:**
    - Identifica cualquier anomalía en los datos, como valores atípicos (outliers) extremos.
    - Señala tendencias o patrones interesantes que observes. Por ejemplo, si hay una correlación fuerte entre dos variables.
    - Destaca cualquier columna categórica o de texto que pueda tener valores inesperados o incoherentes.
    - Menciona si hay duplicados que puedan afectar el análisis.

**Sugerencias para el Usuario:**
    - Basado en el análisis, ofrece al usuario sugerencias concretas para profundizar en el estudio de los datos. 
    Por ejemplo, "Te sugiero que investigues la distribución de la columna 'Ingresos' para entender la variabilidad", 
    o "Podrías limpiar los valores nulos de la columna 'Edad' para un análisis más preciso".

Tu respuesta debe ser clara, relativamente corta y organizada. Utiliza un lenguaje sencillo, evitando la jerga técnica innecesaria. 
El objetivo es que el usuario pueda tomar decisiones informadas sobre sus datos basándose en tu análisis.
"""
