import os
import base64
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

# Initializate analyzer.
dm = DataManager()
# Define page layout.
col1, col2 = st.columns(2)

with col1:
    # Select datafile to load.
    file = st.selectbox("Seleccione un archivo del directorio /data", os.listdir("./data"))

    # Load data and generate report.
    dm.load_data(f"data/{file}")
    report_path = f"reports/{dm.file_name}-report.pdf"
    
    # Display button to generate report.
    with open(report_path, "rb") as f:
        data_pdf = f.read()
    st.download_button(
        label="Obtenga el reporte generado",
        data=data_pdf,
        file_name=f"{dm.file_name}-exported.pdf",
        mime=f"application/pdf",
        icon="📥", 
        use_container_width=True,
    )

with col2:
    # Select format to export data.  
    opt = st.selectbox(
        label="Seleccione un formato para exportar los datos", 
        options=list(constants.FORMAT.keys()),
    )
    
    # Parse selected format and export data.
    file_extension = constants.FORMAT[opt]
    export_path = f"exports/{dm.file_name}-exported{file_extension}"
    if not os.path.exists(export_path): dm.export_data(opt)

    # Access file inside its folder.
    with open(export_path, "rb") as export_file:
        export_data = export_file.read()
    
    # Display download button.
    st.download_button(
        label="Descargue el fichero convertido",
        data=export_data,
        file_name=f"{dm.file_name}-exported{file_extension}",
        mime=f"application/{file_extension}",
        icon="📋", 
        use_container_width=True,
    )
