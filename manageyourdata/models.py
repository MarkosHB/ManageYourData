import pandas as pd
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from manageyourdata.utils import constants


def create_llm_agent(provider: str, model_selected: str, api_key: str = None) -> ChatOllama | ChatGoogleGenerativeAI:
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

    try:
        # "Ollama"
        if provider == constants.MODEL_PROVIDERS[0]:
            llm = ChatOllama(model=model_selected)

        # "Google"
        elif provider == constants.MODEL_PROVIDERS[1]:
            llm = ChatGoogleGenerativeAI(model=model_selected, google_api_key=api_key)

        else:
            raise ValueError(f"Unsupported LLM provider. Supported providers: {constants.MODEL_PROVIDERS}")

    except Exception:
        raise ValueError(f"LLM could not be initialized. Check the configuration information provided.")

    return llm


def create_dataframe_agent(llm: ChatOllama | ChatGoogleGenerativeAI, dataframe: pd.DataFrame) -> AgentExecutor:
    """Create a LangChain Pandas DataFrame agent.

    Args:
        llm: The initialized LLM instance.
        dataframe: The pandas DataFrame to be analyzed.

    Returns:
        agent: The initialized Pandas DataFrame agent.
    """

    agent = create_pandas_dataframe_agent(llm, dataframe, verbose=True, allow_dangerous_code=True)
    return agent


CONFIG_PROMT = """
Eres un analista de datos experto con un conocimiento profundo en el análisis y la interpretación de conjuntos de datos (datasets). 
Tu objetivo es analizar un DataFrame de pandas y extraer métricas con aspectos destacables que sean útiles para un usuario no técnico.
Para facilitar tu tarea, se puede haber precalculado información relevante del mismo en las siguientes variables:
    1. Aspectos generales del conjunto de datos: {general_details} \n
    2. Aspectos concretos sobre cada uno de los atributos: {fields_details} \n
Es recomendable consultar esta información para tus análisis (incluso si el usuario no lo pide explícitamente).

Algunas sugerencias de pasos a seguir pueden ser:

**Visión general del Dataset:**
    - Proporcionar un resumen conciso del dataset.
    - Describir la naturaleza de los datos.

**Métricas Clave:**
    - Descatar anomalías o aspectos interesantes en las principales métricas si es conveniente.

**Aspectos Destacables y Anomalías:**
    - Identificar cualquier anomalía en los datos, como valores atípicos (outliers) extremos.
    - Señalar tendencias o patrones interesantes que observes. Por ejemplo, si hay una correlación fuerte entre dos variables.
    - Destacar cualquier columna categórica o de texto que pueda tener valores inesperados o incoherentes.
    - Mencionar si hay duplicados que puedan afectar el análisis.

**Sugerencias para el Usuario:**
    - Basado en el análisis, ofrece al usuario sugerencias concretas para profundizar en el estudio de los datos. 
    Por ejemplo, "Te sugiero que investigues la distribución de la columna 'Ingresos' para entender la variabilidad", 
    o "Podrías limpiar los valores nulos de la columna 'Edad' para un análisis más preciso".

Tu respuesta debe ser clara, relativamente corta y organizada. Utiliza un lenguaje sencillo, evitando la jerga técnica innecesaria. 
El objetivo es que el usuario pueda tomar decisiones informadas sobre sus datos basándose en tu análisis.
Debes ceñirte en todo momento a lo que el usuario te ha pedido realizar.
"""

PROMPT_TEMPLATE = ChatPromptTemplate(
    messages=[("system", CONFIG_PROMT), MessagesPlaceholder("msgs")],
    input_variables=["general_details", "fields_details", "msgs"],
)
