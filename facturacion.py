import numpy as np
import random
import re


def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"]==tag:
            result = random.choice(i['responses'])
            break
    return result


def facturacion(prediccionCategoria, intents):
	res = get_response(prediccionCategoria, intents)
	print(res)
	print("Me puede indicar su razón social por favor.")
	razon_social = input("")
	print("Gracias!")
	print("En un momento su ejecutivo de ventas se pondrá en contacto con usted para enviarle la información solicitada.")