from flask import Flask, jsonify, request
import hdbcli
from hdbcli.dbapi import connect
from hdbcli import dbapi
from config import HANA_CONFIG
import sett
import services
import procesos

app = Flask(__name__)

def connect_to_hana():
    connection = hdbcli.dbapi.connect(**HANA_CONFIG)
    return connection
@app.route('/')
def index():
    return 'Hola, este es el controlador de inicio.'

@app.route('/api/data', methods=['GET','POST'])
def get_data():
    connection = connect_to_hana()
    cursor = connection.cursor()

    try:
        # Ejecutar una consulta en tu base de datos HANA
        query = "SELECT 'Hello, HANA!' FROM DUMMY"
        cursor.execute(query)

        # Obtener los resultados
        results = cursor.fetchone()

        # Formatear los resultados como JSON y devolverlos
        return jsonify({"data": results[0]})

    finally:
        # Cerrar el cursor y la conexion
        cursor.close()
        connection.close()


@app.route('/bienvenido', methods=['GET','POST'])
def bienvenido():
    return 'Hola mundo, desde Flask'


@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token:
            return request.args.get('hub.challenge'), 200
        else:
            return 'token incorrectos', 200
    except Exception as e:
        return e, 403


@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)

        # Aca deberia ir la interpretacion y luego solo enviar el mensaje resultante

        mensaje = procesos.main_ia(text)

        services.administrar_chatbot(mensaje, number, messageId, name)
        proceso.append(pp)
        return 'enviado'

    except Exception as e:
        return 'no enviado ' + str(e)


if __name__ == '__main__':
    # Debug
    app.run(debug=False, port=5000)
     # Production
    #http_server = WSGIServer(('', 443), app)
    #http_server.serve_forever()