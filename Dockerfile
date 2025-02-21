# Usar una imagen base de Python
FROM python:3.11

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el contenido del proyecto al directorio de trabajo
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar manageyourdata
RUN pip install .

# Exponer el puerto que usará Streamlit
EXPOSE 8501

# Comando para ejecutar la aplicación Streamlit
CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]