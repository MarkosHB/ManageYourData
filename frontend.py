import os
import streamlit as st
from manageyourdata.data_manager import DataManager
from manageyourdata.utils import constants

# Configure the page.
st.set_page_config(
    page_title="ManageYourData - Generate a report of your data", 
    page_icon=":bar_chart:"
)

# Website content display.
st.title(":wave: Bienvenido a :blue[ManageYourData]")
st.image("./manageyourdata/utils/image.jpg")
st.divider()

col1, col2 = st.columns(2)
with col1:
    # Left column. Select datafile to load.
    file = st.selectbox(
        "Seleccione un archivo del directorio /data", os.listdir("./data"))

    dm = DataManager()
    dm.load_data(f"data/{file}")
    
    btn = st.button(
        label="Descargue el reporte generado.",
        on_click=lambda: dm.report_pdf(f"reports/{dm.file_name}-report.pdf"),
        use_container_width=True,
        icon="📥", 
    )
    
with col2:
    # Right column. Select format to export data.
    opt = st.selectbox(
        label="Seleccione un formato para exportar los datos", 
        options=list(constants.FORMAT.keys()),
    )
    
    btn2 = st.button(
        label="Obtenga el fichero convertido.",
        on_click=lambda: dm.export_data(opt),
        use_container_width=True,
        icon="📋", 
    )
