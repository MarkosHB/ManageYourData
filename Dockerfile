# Usar una imagen de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el contenido del proyecto al directorio de trabajo
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar manageyourdata
RUN pip install .

# Exponer los puertos usados
EXPOSE 8000 8501

# Ejecutar FastAPI y Streamlit en paralelo
CMD bash -c "\
  uvicorn api:app --host 0.0.0.0 --port 8000 & \
  streamlit run frontend.py --server.port=8501 --server.address=0.0.0.0"
