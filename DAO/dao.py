import mysql.connector
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from datetime import datetime, date
import json

class CustomJSONEncoder(json.JSONEncoder): # Creamos esta clase para poder serializar el tipo DATE de MySQL a JSON
    def default(self, obj): # Redefinimos su método default para que se ajuste a lo que necesitamos
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        else:
            return super().default(obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder  # Utilizamos nuestro serializador personalizado
api = Api(app)

class DAO_noticias(Resource):
    def __init__(self):
        self.db = mysql.connector.connect(
            host='database',
            port='3306',
            user='root',
            password='root_password',
            database='notibolt'
        )
        self.cursor = self.db.cursor()
        
    def get(self):
        query = "SELECT * FROM noticias"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        # Obtener los nombres de las columnas
        columns = [desc[0] for desc in  self.cursor.description]

        # Construir la lista de noticias
        news = []
        for row in result:
            news.append(dict(zip(columns, row)))

        return jsonify(news) # Codificamos la respuesta SQL como JSON

class DAO_usuarios(Resource):
    def __init__(self):
        self.db = mysql.connector.connect(
            host='database',
            port='3306',
            user='root',
            password='root_password',
            database='notibolt'
        )
        self.cursor = self.db.cursor()
    
    def get(self):
        query = "SELECT * FROM usuarios"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        # Obtener los nombres de las columnas
        columns = [desc[0] for desc in  self.cursor.description]
        # Construir la lista de noticias
        usuarios = []
        for row in result:
            usuarios.append(dict(zip(columns, row)))
        return jsonify(usuarios) # Codificamos la respuesta SQL como JSON
    
    def post(self):
        data = request.get_json()  # Obtener los datos enviados en el cuerpo de la solicitud
        # Insertamos el nuevo usuario
        nombre = data.get('nombre')
        correo = data.get('correo')
        contrasegna = data.get('contrasegna')
        # Insertamos en la base de datos
        query = "INSERT INTO usuarios (nombre, correo, contrasegna) VALUES (%s, %s, %s)"
        values = (nombre, correo, contrasegna)
        self.cursor.execute(query, values)
        self.db.commit()

api.add_resource(DAO_noticias, '/DAO_noticias', methods=['GET', 'POST'])
api.add_resource(DAO_usuarios, '/DAO_usuarios', methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
