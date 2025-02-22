import os
import base64
import streamlit as st
from manageyourdata.data_manager import DataManager
from manageyourdata.utils import constants


def display_pdf(file_path):
    """Show a PDF inside a iframe in Streamlit."""
    
    with open(file_path, "rb") as f:
        b64_pdf = base64.b64encode(f.read()).decode()
    
    pdf_display = f"""
    <div style="margin-top: 40px;">
        <iframe 
            src="data:application/pdf;base64,{b64_pdf}" 
            width="100%"
            height="700" 
            style="border: none;">
        </iframe>
    </div>
    """
    return pdf_display


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
    if st.button(label="Obtenga el reporte generado", use_container_width=True, icon="📥"):
        if not os.path.exists(report_path): dm.report_pdf(report_path)
        st.session_state.show_pdf = True
    else:
        st.session_state.show_pdf = False
    
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

# Display PDF report if needed.
if "show_pdf" in st.session_state and st.session_state.show_pdf:
    st.markdown(display_pdf(report_path), unsafe_allow_html=True)
