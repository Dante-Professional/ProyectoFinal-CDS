# Imagen base de Python
FROM python:3.11.3

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos al directorio de trabajo
COPY requirements.txt .

# Instala los requerimientos
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del directorio "Consumer" en el directorio de trabajo
COPY . .

# Exponemos el número de puerto
EXPOSE 5002

# Ejecuta el archivo "consumer.py" al iniciar el contenedor
CMD ["python", "bll.py"]
