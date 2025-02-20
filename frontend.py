import os
import streamlit as st
from manageyourdata.data_manager import DataManager
from manageyourdata.utils import constants

st.set_page_config(
    page_title="ManageYourData - Generate a report of your data", 
    page_icon=":bar_chart:"
)

# Website content display.
st.title(":wave: Bienvenido a :blue[ManageYourData]")
st.divider()

formatos_aceptados = ", ".join(constants.FORMAT.values())
st.info(f"Actualmente son aceptados los siguientes formatos de fichero de datos: {formatos_aceptados}", icon="ℹ️")

uploaded_file = st.file_uploader("empty", accept_multiple_files=False, label_visibility="collapsed")
if uploaded_file is not None:

    if not os.path.exists("data"):
        os.makedirs("data")

    # Guardar el archivo subido en el sistema de archivos temporalmente
    with open(os.path.join("data", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Obtener la ruta del archivo guardado
    file_path = os.path.join("data", uploaded_file.name)
    
    try:
        dm = DataManager()
        dm.load_data(file_path)
        dm.report_pdf("reports/report.pdf")

        with open("reports/report.pdf", "rb") as file:
            btn = st.download_button(
                label="Descargue el reporte generado por la herramienta",
                data=file,
                file_name="report.pdf",
                mime="application/pdf",
                icon="📥", 
                use_container_width=True,
            )
    except Exception as e:
        st.error(f"Ha ocurrido un error: El formato proporcionado no es adecuado.")

    