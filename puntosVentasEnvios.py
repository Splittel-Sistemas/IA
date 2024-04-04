import numpy as np
import random


def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"]==tag:
            result = random.choice(i['responses'])
            break
    return result

def puntosVentasEnvios(prediccionCategoria, intents):
	res = get_response(prediccionCategoria, intents)
	print(res)
	print("Nuestro punto de ventas fisico se encuetra en:")
	print("Queretaro, México.")
	print("Contamos con envio a toda la Republica Mexicana.")
	print("También contamos con envios internacionales.")