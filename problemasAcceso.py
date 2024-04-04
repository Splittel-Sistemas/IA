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


def problemas_acceso(prediccionCategoria, intents):
	res = get_response(prediccionCategoria, intents)
	print(res)
	razon_social = input("")
	print("Lo voy a comunicar con un asesor, ya que es necesario validar cierta información, en unos momentos se pondrá en contacto con usted.")