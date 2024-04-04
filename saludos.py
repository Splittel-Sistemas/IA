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


def saludos(prediccionCategoria, intents):
    res = get_response(prediccionCategoria, intents)
    print(res)
    nombre = input("")
    print("En que le puedo ayudar el dia de hoy, " + nombre + "?")
    mensaje = input("")
    return mensaje, nombre