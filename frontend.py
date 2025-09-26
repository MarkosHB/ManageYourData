import os
import json
import streamlit as st
from manageyourdata.data_manager import DataManager
from manageyourdata.utils import constants


# Configure the page.
st.set_page_config(
    page_title="ManageYourData",
    page_icon=":bar_chart:",
    initial_sidebar_state="expanded"
)

# Initialize session state for data managers.
if "data_managers" not in st.session_state:
    st.session_state.data_managers = {}


#########################
# Slider content display.
#########################

with st.sidebar:
    st.title("⚙️ Configuración")

    # Determine llm provider.
    provider = st.selectbox(
        label="Proveedor de LLM",
        options=constants.MODEL_PROVIDERS,
    )

    if provider == "Google":
        st.warning("Aviso: El análisis dejará de ser local", icon="⚠️")

        # Obtain model name from user input.
        model_selected = st.text_input(
            label="Modelo elegido", 
            help="Listado de modelos disponibles en https://ai.google.dev/gemini-api/docs/models",
            value="gemini-2.5-flash",
        )

        # Input for Google API key.
        api_key = st.text_input(
            label="Clave de la API de Google",
            type="password",
            value=st.session_state.get("api_key", ""),
            help="Puede obtener su clave en https://aistudio.google.com/app/apikey"
        )

        # Save api_key in memory.
        if api_key not in st.session_state:
            st.session_state.api_key = api_key

        # Option to set API key as environment variable.
        set_env = st.checkbox("Establecer como variable de entorno", value=True)
        if set_env:
            os.environ["GOOGLE_API_KEY"] = api_key

    elif provider == "Ollama":
        api_key = None

        # Obtain model name from user input.
        model_selected = st.text_input(
            label="Modelo elegido",
            value="llama3.2",
            help="Listado de modelos disponibles en https://ollama.com/search",
        )


    st.divider()

    st.title("📋 Sistema de ficheros")

    # Allow user data file to be inside /data folder.
    uploaded_file = st.file_uploader(
        label="Proporcione su fichero de datos o colóquelo en :blue[/data]",
        type=constants.FORMAT.keys(),
    )

    if uploaded_file is not None:
        # Get the new file name.
        file_name = uploaded_file.name
        # Create the full path to save the file.
        save_path = os.path.join("./data", file_name)

        # Open the file and write the content.
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())


    # Display contents of folders.
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


col1, col2 = st.columns(2)
with col1:
    # Select datafile to load.
    file = st.selectbox(
        label="Seleccione un archivo de datos.",
        help="Los archivos listados se encuentran en el directorio :blue[/data]",
        placeholder="Sin opción elegida",
        options=os.listdir("./data"),
        index=None,
    )

    if file:
        if file not in st.session_state.data_managers:
            st.session_state.data_managers[file] = DataManager()

        # Parse data input.
        st.session_state.data_managers[file].load_data(f"data/{file}")
        report_path = f"reports/{st.session_state.data_managers[file].file_name}-report.pdf"

        # Display button to generate report.
        if st.button(label="Generar reporte PDF", icon="🛠️", use_container_width=True):
            st.session_state.data_managers[file].report_pdf(report_path)
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
        if st.button(label="Convertir fichero de datos", icon="🛠️", use_container_width=True):
            st.session_state.data_managers[file].export_data(opt)
            st.rerun()
            st.toast("Fichero de datos convertido correctamente", icon="✅")


#######################
# Tabs content display.
#######################

if file and provider:
    # Create tabs to display PDF report and ask questions.
    tab1, tab2 = st.tabs(["Conversar con los datos", "Visualizar reporte PDF"])

    with tab1:
        # Display the chat messages from history on app rerun.
        for message in st.session_state.data_managers[file].get_historic():
            with st.chat_message(message.type):
                st.markdown(message.content)
        
        # Make sure there's an api key when needed.
        check_disabled = provider != constants.MODEL_PROVIDERS[0] and not api_key
        if not check_disabled:
            # Determine the assistant to use.
            st.session_state.data_managers[file].create_assistant(provider, model_selected, api_key)

        # Retrieve question from user.
        if prompt := st.chat_input("¿Qué quieres descubrir hoy sobre tus datos?", disabled=check_disabled):
            
            with st.spinner("Analizando datos..."):
                try:
                    # Ask the assistant.
                    _ = st.session_state.data_managers[file].chat_with_assistant(prompt)
                
                    # Refresh chat messages display.
                    st.rerun()

                except Exception as e:
                    st.error(e)

        # Utilities buttons.
        col1, col2 = st.columns(2)

        with col1:
            # Parse historic to be JSON serializable.
            serializable_history = [
                {"type": msg.type, "content": msg.content} 
                for msg in st.session_state.data_managers[file].get_historic()
            ]
            # Allow user to obtain the record.
            btn = st.download_button(
                label="Guardar conversación",
                data=json.dumps(serializable_history, indent=1, ensure_ascii=False),
                file_name="conversacion.json",
                mime="application/json",
                icon="💾", 
                use_container_width=True
            )

        with col2:
            # Allow user to clear the chat.
            if st.button("Borrar chat actual", icon="🗑️", use_container_width=True):
                st.session_state.data_managers[file].delete_historic()
                # Banish conversation from screen. 
                st.rerun()
    
    with tab2:
        # Display PDF download button and report.
        if os.path.exists(report_path):
            st.pdf(report_path, height=850)
            with open(report_path, "rb") as pdf:
                btn = st.download_button(
                    label="Descárguelo pulsando aquí",
                    data=pdf,
                    file_name="report.pdf",
                    mime="application/pdf",
                    icon="📥", 
                )
        else:
            st.info("Genere primero el reporte PDF para visualizarlo aquí.")
