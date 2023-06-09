# Imagen base de Python
FROM python:3.11.3

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos al directorio de trabajo
COPY requirements.txt .

# Instala los requerimientos
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del directorio "Producer" en el directorio de trabajo
COPY . .

# Ejecuta el archivo "producer.py" al iniciar el contenedor
CMD ["python", "producer_service.py"]
