import time
import requests
import json
from kafka import KafkaProducer
from datetime import datetime, timedelta

time.sleep(80) # Realizamos una pequeña espera para que espere al resto de contenedores

# Configuración de Kafka
KAFKA_TOPIC = "test-topic"
KAFKA_BOOTSTRAP_SERVERS = ["kafka:9092"]
producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

API_POLL_INTERVAL = 30  # Segundos

def main():
    primera_ejecucion = True
    while True:
        if primera_ejecucion:
            fecha = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') # Generamos la fecha de ayer
            primera_ejecucion = False
        else:
            fecha = (datetime.now()).strftime('%Y-%m-%d') # Generamos la fecha actual
        
        # Creamos y ejecutamos la consulta a la API
        API_URL = ('https://newsapi.org/v2/everything?'
                    'q=*&'
                    'from='+fecha+'&'
                    'language=es&'
                    'apiKey=1a8743b722734cd88527d94e98154466')

        response = requests.get(API_URL)
        data = response.json()
        
        producer.send(KAFKA_TOPIC, value=data) # Enviamos los datos a Kafka

        time.sleep(API_POLL_INTERVAL) # Esperamos el tiempo definido para la siguiente consulta

if __name__ == "__main__":
    main()