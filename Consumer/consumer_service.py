import json
import time
import mysql.connector
from kafka import KafkaConsumer
from datetime import datetime

time.sleep(80) # Realizamos una pequeña espera para que espere al resto de contenedores

db_config = {
    'host': 'database',
    'port': '3306',
    'user': 'root',
    'password': 'root_password',
    'database': 'notibolt'
}

# Consumimos datos de Kafka¡
try:
    consumer = KafkaConsumer('test-topic', bootstrap_servers=['kafka:9092'])
    for message in consumer:
        # Configuramos la conexión a la base de datos
        db = mysql.connector.connect(**db_config)

        # Creamos un cursor para la conexión a la base de datos
        cursor = db.cursor()

        # Decodificamos el mensaje y lo cargamos como un objeto 
        datos_json = json.loads(message.value.decode('utf-8'))

        # Iteramos sobre todas las noticias en el mensaje de Kafka
        for article in datos_json['articles']:
            fecha_noticia = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S') # Ajustamos el formato de fecha correctamente

            # Comprobamos si existe la noticia antes de insertar en la base de datos
            sql = "SELECT url FROM noticias WHERE url = %s"
            data = (article['url'],) # Se agrega una coma porque execute espera una tupla
            cursor.execute(sql, data)
            result = cursor.fetchone() # Nos un resultado en caso de existir

            if result is None: # Si no hay resultado -> insertamos
                sql = "INSERT INTO noticias (titulo, contenido, fecha_noticia, autor, url) VALUES (%s, %s, %s, %s, %s)"
                data = (article['title'], article['description'], fecha_noticia, article['author'], article['url'])
                cursor.execute(sql, data)
                db.commit()

        # Cerramos el cursor y la conexión a la base de datos
        cursor.close()
        db.close()

except Exception as error:
    print(f"Error al consumir datos de Kafka: {error}")