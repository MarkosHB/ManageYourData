import os
import json
import streamlit as st
from manageyourdata.data_manager import DataManager
from manageyourdata.utils import constants
from manageyourdata.models import create_llm_agent
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


# Configure the page.
st.set_page_config(
    page_title="ManageYourData",
    page_icon=":bar_chart:",
    initial_sidebar_state="expanded"
)

if "messages" not in st.session_state:
    st.session_state.messages = []


#########################
# Slider content display.
#########################

with st.sidebar:
    st.title("⚙️ Configuración")

    # Get Google API key from user.
    provider = st.selectbox(
        label="Proveedor de LLM",
        options=constants.MODEL_PROVIDERS,
    )

    if provider == "Google":
        st.warning("Aviso: El análisis dejará de ser local", icon="⚠️")
        # Input for Google API key.
        api_key = st.text_input(
            label="Clave de la API de Google",
            type="password",
            help="Puede obtener su clave en https://aistudio.google.com/app/apikey"
        )

        if api_key not in st.session_state:
            st.session_state.api_key = api_key

        # Option to set API key as environment variable.
        set_env = st.checkbox("Establecer como variable de entorno", value=True)
        if set_env:
            os.environ["GOOGLE_API_KEY"] = api_key

    elif provider == "Ollama":
        api_key = None
        st.text("Asegúrate de tener Ollama instalado y un modelo descargado.",
                help="Más info en https://ollama.com/docs/installation")

    st.divider()

    st.title("📋 Sistema de ficheros")
    st.subheader("Contenido de la carpeta :blue[/data]")
    st.write(os.listdir("./data"))
    st.subheader("Contenido de la carpeta :blue[/reports]")
    st.write(os.listdir("./reports"))
    st.subheader("Contenido de la carpeta :blue[/exports]")
    st.write(os.listdir("./exports"))

    st.divider()

    st.title("📚 Referencias")
    st.link_button(label="Repositorio de Github", url=f"{constants.GITHUB_URL}", icon="🔗")
    st.image("./manageyourdata/utils/image.jpg")


############################
# Main page content display.
############################

st.title(":wave: Bienvenido a :blue[ManageYourData]")
st.subheader("Gestiona y analiza tus datos en local de forma sencilla.")
st.divider()


# Basic operations.
dm = DataManager()
col1, col2 = st.columns(2)

with col1:
    # Select datafile to load.
    file = st.selectbox(
        label="Seleccione un archivo de datos.",
        help="Los archivos listados se encuentran en el directorio :blue[/data]",
        placeholder="Sin opción elegida",
        options=os.listdir("./data"),
        index=None,
        on_change=st.session_state.messages.clear,
    )

    if file:
        # Parse data input.
        dm.load_data(f"data/{file}")
        report_path = f"reports/{dm.file_name}-report.pdf"

        # Display button to generate report.
        if st.button(label="Generar reporte PDF", icon="🛠️"):
            dm.report_pdf(report_path)
            st.rerun()
            st.toast("Reporte PDF generado correctamente", icon="✅")

with col2:
    # Select format to export data.
    opt = st.selectbox(
        label="Seleccione un formato para exportar.",
        help="Debe de haber elegido un archivo de datos previamente",
        placeholder="Sin opción elegida",
        options=list(constants.FORMAT.keys()),
        index=None,
    )

    if opt and file:
        # Display button to export data.
        if st.button(label="Convertir fichero de datos", icon="🛠️"):
            dm.export_data(opt)
            st.rerun()
            st.toast("Fichero de datos convertido correctamente", icon="✅")

st.divider()

#######################
# Tabs content display.
#######################

if file and provider:
    # Create tabs to display PDF report and ask questions.
    tab1, tab2, tab3 = st.tabs(
        ["Visualizar reporte PDF", "Conversar con los datos", "Historial de conversación"])

    with tab1:
        # Display PDF download button and report.
        if os.path.exists(report_path):
            st.pdf(report_path, height=850)
            with open(report_path, "rb") as file:
                btn = st.download_button(
                    label="Descárguelo pulsando aquí",
                    data=file,
                    file_name="report.pdf",
                    mime="application/pdf",
                    icon="📥", 
                )
        else:
            st.info("Genere primero el reporte PDF para visualizarlo aquí.")

    with tab2:  
        # Make sure there's an api key when needed.
        check_disabled = provider != constants.MODEL_PROVIDERS[0] and not api_key
        
        # Retrieve question from user.
        st.container()
        if prompt := st.chat_input("¿Qué quieres descubrir hoy?", disabled=check_disabled):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                llm = create_llm_agent(provider, api_key)
                # Create agent instance.
                agent = create_pandas_dataframe_agent(llm, dm.data, verbose=True, allow_dangerous_code=True)
                # Generate response.
                response = agent.invoke(prompt)
                st.markdown(response["output"])
            st.session_state.messages.append({"role": "assistant", "content": response["output"]})

        btn = st.download_button(
                    label="Guardar conversación",
                    data=json.dumps(st.session_state.messages),
                    file_name="conversacion.json",
                    mime="application/json",
                    icon="💾", 
                )
        
    with tab3:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
