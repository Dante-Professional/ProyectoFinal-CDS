import requests
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS  # Importa el middleware de CORS

app = Flask(__name__)
api = Api(app)
CORS(app)  # Agrega el middleware de CORS a la aplicación

@app.route('/obtenerNoticias', methods=['GET'])
def obtener_noticias():
    response = requests.get('http://dao:5001/DAO_noticias')
    result = response.json()
    # Aplicamos la lógica de negocio a los datos
    sorted_result = sorted(result, key=lambda x: x['id_noticia'], reverse=True)  # Ordenar por id ya que las últimas son las más nuevas
    limited_result = sorted_result[:3]  # Limitar a las primeras 4 noticias
    return limited_result

@app.route('/registrarUsuario', methods=['POST'])
def registrar_usuario():
    data = request.json  # Obtenemos todos los datos enviados en el formulario de registro
    correo = data.get('correo') # Guardamos este valor únicamente porque es el que utilizaremos para comprobar la existencia

    response = requests.get('http://dao:5001/DAO_usuarios') # Recibimos los usuarios de DAO
    result = response.json()

    # Verificamos si el correo existe en el resultado
    correo_existente = False
    for usuario in result:
        if usuario['correo'] == correo:
            correo_existente = True
            return jsonify({'mensaje': 'El correo introducido ya existe'})
    
    if correo_existente == False:
        response = requests.post('http://dao:5001/DAO_usuarios', json=data) # Enviamos los datos a la API DAO
        return jsonify({'mensaje': 'Registro completado'})

@app.route('/iniciarUsuario', methods=['POST'])
def iniciar_usuario():
    data = request.json  # Obtenemos todos los datos enviados en el formulario de registro
    correo = data.get('correo')
    contrasegna = data.get('contrasegna')

    response = requests.get('http://dao:5001/DAO_usuarios') # Recibimos los usuarios de DAO
    result = response.json()

    # Verificamos si el correo existe en el resultado
    usuario_existente = False
    for usuario in result:
        if (usuario['correo'] == correo) and (usuario['contrasegna'] == contrasegna):
            usuario_existente = True
            break
    
    if usuario_existente == True:
        return jsonify({'mensaje': 'Sesión iniciada'})
    else:
        return jsonify({'mensaje': 'Datos introducidos incorrectos'})

@app.route('/busqueda', methods=['POST'])
def buscar():
    data = request.json  # Obtenemos todos los datos enviados en el buscador
    busqueda = data.get('busqueda')

    response = requests.get('http://dao:5001/DAO_noticias') # Recibimos las noticias de DAO
    result = response.json()

    noticias_filtradas = []
    for noticia in result:
        if noticia.get('autor') == busqueda:
            noticias_filtradas.append(noticia)

    return jsonify(noticias_filtradas)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
