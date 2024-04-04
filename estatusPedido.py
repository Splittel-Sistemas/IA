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

def estatus_Pedido(prediccionCategoria, intents):
	res = get_response(prediccionCategoria, intents)
	print(res)
	print("Me puede apoyar con los siguientes datos por favor:")
	print("Número de pedido:")
	n_pedido = input("")
	print("Número de teléfono:")
	n_telefono = input("")
	print("Muchas gracias!, en un momento su ejecutivo de ventas se estará comunicando con usted para brindarle más información acerca de su pedido.")
	print("Por el momento, este es su número de guia por si desea rastrear su pedido.")
