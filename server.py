from flask import Flask, request
import sett 
import services
import procesos
import numpy as np



ia = procesos.d_flow()
ia.vIniciales()

app = Flask(__name__)

@app.route('/bienvenido', methods=['GET'])
def  bienvenido():
    return 'Hola mundo, desde Flask'

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge != None:
            return challenge
        else:
            return 'token incorrecto', 403
    except Exception as e:
        return e,403
    
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
        
        
        mensaje, acciones = ia.main_ia(text)
        services.administrar_chatbot(mensaje, number,messageId,name, acciones)
        save_message = name + ": " + text 
        for item in mensaje:
            save_message = save_message + "\n" + "Raul: " + item 

        ia.conversacion_ia(save_message, number)
        
      
        return 'enviado'

    except Exception as e:
        return 'no enviado ' + str(e)

if __name__ == '__main__':

    app.run(debug=False, port=5000)
