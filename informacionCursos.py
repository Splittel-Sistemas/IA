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

def informacionCursos(prediccionCategoria, intents):
	res = get_response(prediccionCategoria, intents)
	print(res)
	print("Puede consultar nuestros seminarios online gratuitos en el siguiente link:")   #hacer consulta
	print("https://fibremex.com/fibra-optica/views/Capacitaciones/2-seminarios-online")
	print("Para incribirse a cualquiera de nuestros seminarios online solo debe llenar el formato que se encuentra en el link que le proporcione.")
	print("Puede consultar nuestros cursos presenciales en el siguiente link:")
	print("https://fibremex.com/fibra-optica/views/Capacitaciones/3-cursos-presenciales-fibra-optica")
	print("Para inscribirse a cualquiera de nuestros cursos presenciales debe llenar los datos requeridos en el link proporicionado,")
	print("posteriormente, un asesor se pondrá en contacto con usted para darle mas detalles de la inscripción.")
	print("*Todos los cursos presenciales son impartidos en la ciudad de Queretaro.")


