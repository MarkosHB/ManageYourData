import os
from fastapi import FastAPI, HTTPException
from manageyourdata.data_manager import DataManager
from manageyourdata.utils import constants

app = FastAPI()
dm = DataManager()


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de ManageYourData."}


@app.get("/files")
def list_files():
    """Lista los archivos disponibles en el directorio /data."""
    try:
        files = os.listdir("./data")
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/load-data/")
def load_data(file_name: str):
    """Carga un archivo de datos desde el directorio /data."""
    try:
        file_path = f"./data/{file_name}"
        dm.load_data(file_path)
        return {"message": f"Archivo {file_name} cargado correctamente."}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo no encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-report/")
def generate_report():
    """Genera un informe PDF del archivo cargado."""
    try:
        if not dm.file_name:
            raise HTTPException(status_code=400, detail="No se ha cargado ningún archivo.")
        report_path = f"./reports/{dm.file_name}-report.pdf"
        dm.report_pdf(report_path)
        return {"message": f"Informe generado correctamente en {report_path}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/export-data/")
def export_data(format: str):
    """Exporta los datos cargados en el formato especificado."""
    try:
        if not dm.file_name:
            raise HTTPException(status_code=400, detail="No se ha cargado ningún archivo.")
        if format not in constants.FORMAT:
            raise HTTPException(status_code=400, detail="Formato no soportado.")
        file_extension = constants.FORMAT[format]
        export_path = f"./exports/{dm.file_name}-exported{file_extension}"
        dm.export_data(format)
        return {"message": f"Datos exportados correctamente en {export_path}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
