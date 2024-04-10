import requests
import sett
import json
import time


def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def send_contact(number, name, lastName, phoneNumber, email_):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "contacts",
            "contacts": [{
                "emails": [{
                    "email": email_
                }],
                "name": {
                    "formatted_name": name + " " + lastName,
                    "first_name": name,
                    "last_name": lastName
                },
                #"org": {
                 #   "company": "Splittel"
                #},
                "phones":[{
                    "phone": phoneNumber,
                    #"wa-id": "+52" + phoneNumber,
                    "type": "Móvil"
                }
                ]
            }
            ]
            
        }
    )
    return data

def send_location(number, longitude, latitude, name, address_):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "location",
            "location": {
                "longitude": longitude,
                "latitude": latitude,
                "name": name,
                "address": address_,
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def administrar_chatbot(text,number, messageId, name,acciones):
    #text = text.lower() #mensaje que envio el usuario
    list = []
    print("mensaje del usuario: ",text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    #time.sleep(1)

    #data = text_Message(number, text)
    #print(len(text))



    if acciones == "enviarCatalogo":

        #url = "C:/Users/Maritza González/PruebasMaritza/chatbot/chatbot_Raul/hatsapp_api"
        #url = "CatalogoTelecomunicacionesFibremex.pdf"
        #url = "https://publicaciones.fibremex.com/catalogo-telecomunicaciones-fibremex.pdf"
        url = "https://optronics.com.mx/conectividad/public/file/enciclopedia/folleto/Folleto%20Cables%20ADSS%20-%20Optronics.pdf"
        #url = "http://catarina.udlap.mx/u_dl_a/tales/documentos/lem/ledesma_e_ro/capitulo1.pdf"
        caption = "Catalogo Fibremex 2024"
        filename = "catalogoFibremex.pdf"
        data_catalogo = document_Message(number, url, caption, filename)
    elif acciones == "enviarContacto":
        name = "Miguel"
        lastName = "Rosiles"
        phoneNumber = "+524421418496"
        email_ = "miguelrosiles@splittel.com"
        data_contacto = send_contact(number, name, lastName, phoneNumber, email_)

    elif acciones == "reaccionSaludo":
        replyReaction = replyReaction_Message(number, messageId, "👍")
        list.append(replyReaction)

    elif acciones =="enviarUbicacion":
        latitude = 20.555108134187922
        longitude = -100.27050119186629
        name = "Fibremex SA de CV"
        address_ = "Parque Tecnológico Innovación Querétaro Lateral de la carretera Estatal 431, km.2+200, Int.28, 76246 Santiago de Querétaro, Querétaro, México."
        data_ubicaciones = send_location(number, longitude, latitude, name, address_)
        


    sleep_ = 1
    for mensaje in text:
        if mensaje == "Le compartimos nuestro catalogo digital." and acciones == "enviarCatalogo":
            #print("entro")
            list.append(data_catalogo)
            sleep_ = 2
            #print(data_catalogo)
        elif mensaje == "En un momento su ejecutivo de ventas se pondrá en contacto con usted para atenderlo." and acciones == "enviarContacto":
            list.append(data_contacto)
            #sleep_ = 1

        elif mensaje == "Parque Tecnológico Innovación Querétaro, Lateral de la carretera Estatal 431, km.2+200, Int.28, C.P.76246" and acciones == "enviarUbicacion":
            list.append(data_ubicaciones)
            sleep_ = 1

        data = text_Message(number, mensaje)
        list.append(data)

        
        
    
    for item in list:
        enviar_Mensaje_whatsapp(item)
        time.sleep(sleep_)
      
    return 


#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    number = s[3:]
    if s.startswith("521"):
        return "52" + number
    elif s.startswith("549"):
        return "54" + number
    else:
        return s
        

