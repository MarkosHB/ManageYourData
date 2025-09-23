import os
import streamlit as st
from manageyourdata.data_manager import DataManager
from manageyourdata.utils import constants
from manageyourdata.models import create_llm_agent, get_frontend_info
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


def interactive_file_tree(path):
    """Generates an interactive file tree with checkboxes for file deletion."""
    for root, dirs, files in os.walk(path, topdown=True):
        # Sort directories and files for consistent order
        dirs.sort()
        files.sort()

        # Exclude __pycache__ from the listing
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")

        level = root.replace(path, "").count(os.sep)
        indent = "    " * level

        # Display the directory
        if level == 0:
            st.write(f"📁 {os.path.basename(path)}")
        else:
            st.write(f"{indent}📁 {os.path.basename(root)}")

        # Display files with checkboxes
        sub_indent = "    " * (level + 1)
        for f in files:
            file_path = os.path.join(root, f)
            st.checkbox(f"{sub_indent}📄 {f}", key=file_path)


# Configure the page.
st.set_page_config(
    page_title="ManageYourData",
    page_icon=":bar_chart:",
    initial_sidebar_state="expanded"
)


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

        # Option to set API key as environment variable.
        set_env = st.checkbox(
            "Establecer como variable de entorno", value=True)
        if set_env:
            os.environ["GOOGLE_API_KEY"] = api_key

    elif provider == "Ollama":
        api_key = None
        st.text("Asegúrate de tener Ollama instalado y un modelo descargado.",
                help="Más info en https://ollama.com/docs/installation")

    st.divider()

    st.title("📋 Estructura del proyecto")

    # Create a form to contain the file tree and the delete button
    with st.form(key="file_delete_form"):
        dirs_to_show = ["data", "reports", "exports"]
        for directory in dirs_to_show:
            if os.path.isdir(directory):
                interactive_file_tree(directory)
        submit_button = st.form_submit_button(
            label="Eliminar archivos seleccionados")

    if submit_button:
        files_to_delete = [
            key for key, value in st.session_state.items() if value and os.path.isfile(key)]

        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                st.success(f"Eliminado: {file_path}")
                # Uncheck the box after deletion
                st.session_state[file_path] = False
            except Exception as e:
                st.error(f"Error al eliminar {file_path}: {e}")

        # Rerun to update the file tree display
        st.rerun()

    st.image("./manageyourdata/utils/image.jpg")
    st.link_button(label="Repositorio de Github", url=f"{constants.GITHUB_URL}", icon="🔗")


############################
# Main page content display.
############################

st.title(":wave: Bienvenido a :blue[ManageYourData]")
st.text("Una herramienta para gestionar y analizar tus datos en local de forma sencilla.")

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
    tab1, tab2 = st.tabs(["❓ Conversar con el archivo de datos", "📄 Visualizar reporte PDF",])


    with tab1:
        # Get question from user.
        user_question = st.text_input(
            label="Escriba su pregunta sobre el conjunto de datos seleccionado.",
            placeholder="Ej: ¿Cuántos valores nulos existen en mis datos?"
        )

        # Make sure there's an api key when needed.
        button_disabled = (provider != constants.MODEL_PROVIDERS[0] and not api_key)
        # Obtain button configuration details.
        config = get_frontend_info(provider)

        if st.button(label=config["label"], icon=config["icon"], help=config["help"], disabled=button_disabled):
            # Create the llm instance.
            llm = create_llm_agent(provider, api_key)
            # Create agent instance.
            agent = create_pandas_dataframe_agent(llm, dm.data, verbose=True, allow_dangerous_code=True)
            # Generate response.
            response = agent.invoke(user_question)
            # Display response.
            st.write(response)

    with tab2:
        # Display PDF report.
        if os.path.exists(report_path):
            st.pdf(report_path, height=850)
        else:
            st.info("Genere primero el reporte PDF para visualizarlo aquí.")
