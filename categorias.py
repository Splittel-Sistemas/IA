import numpy as np
import random
from informacionCursos import*
from cotizaciones import*
from cursosSeminariosConstancias import*
from servicios import*
from estatusPedido import*
from facturacion import*
from problemasAcceso import*
from catalogo import*
from puntosVentasEnvios import*


#Obtenemos una respuesta aleatoria
def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"]==tag:
            result = random.choice(i['responses'])
            break
    return result

def categoria(prediccionCategoria, intents, message):
	val_return = 1

	if prediccionCategoria == "cotizaciones":
		cotizaciones(message)

	elif prediccionCategoria == "catalogo":
		res = get_response(prediccionCategoria, intents)
		print(res)
		catalogo(prediccionCategoria,intents)

	elif prediccionCategoria == "informacion_cursos":
		informacionCursos(prediccionCategoria, intents)

	elif prediccionCategoria == "cursos_seminarios_constancias":
		cursos_seminarios_constancias(prediccionCategoria, intents)

	elif prediccionCategoria == "facturacion":
		facturacion(prediccionCategoria, intents)

	elif prediccionCategoria == "problemas_acceso":
		problemas_acceso(prediccionCategoria, intents)

	elif prediccionCategoria == "servicios":
		servicios(prediccionCategoria, intents)

	elif prediccionCategoria == "estatusPedido":
		estatus_Pedido(prediccionCategoria, intents)

	elif prediccionCategoria == "puntos_ventas_envios":
		puntosVentasEnvios(prediccionCategoria, intents)

	elif prediccionCategoria == "badWords":
		res = get_response(prediccionCategoria, intents)
		print(res)
		val_return = -1

	elif prediccionCategoria == "final":
		res = get_response(prediccionCategoria, intents)
		print(res)
		val_return= -1

	return val_return

