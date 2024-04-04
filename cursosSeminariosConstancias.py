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



def cursos_seminarios_constancias(prediccionCategoria, intents):

	res = get_response(prediccionCategoria, intents)
	print(res)
	email_valido = 0
	while email_valido == 0:
	    user_input = input()
	    email_constancia = user_input

	    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")

	    if not re.fullmatch(pattern, email_constancia):
	        print("Por favor ingrese una direccion de correo valida.")
	    else:
	        email_valido = 1
	print("Le enviaremos su constancia al correo: " + str(email_constancia) )
	print("Por favor revise su bandeja de SPAM.")