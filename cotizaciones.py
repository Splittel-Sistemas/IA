import random
import json
import pickle
import numpy as np
import re

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

from categorias import*
lemmatizer = WordNetLemmatizer()
#Importamos los archivos generados en el código anterior
intents = json.loads(open('cotizaciones.json').read())
words = pickle.load(open('words_cotizaciones.pkl', 'rb'))
classes = pickle.load(open('classes_cotizaciones.pkl', 'rb'))
model = load_model('cotizaciones_model.h5')
#Pasamos las palabras de oración a su forma raíz
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

#Convertimos la información a unos y ceros según si están presentes en los patrones
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i]=1
    #print(bag)
    return np.array(bag)

#Predecimos la categoría a la que pertenece la oración
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]), verbose=0)[0]
    max_index = np.where(res ==np.max(res))[0][0]
    category = classes[max_index]
    return category


def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"]==tag:
            result = random.choice(i['responses'])
            break
    return result

def cotizaciones(message):

    cotizacion = message
    respuesta = predict_class(cotizacion.lower())
    #res = get_response(respuesta, intents)
    print("Antes de continuar, ha comprado anteriormente con nosotros?")
    mensaje=input("")
    respuesta = predict_class(mensaje.lower())
    res = get_response(respuesta, intents)
    print(res)

    if respuesta == "si":
        print("RFC:")   #validar cliente
        rfc = input("")

    elif respuesta == "no":
        print("Para brindarle un mejor servicio y ponerlo en contacto con un ejecutivo de ventas, me podria brindar los siguientes datos por favor!")
        print("Nombre de Facturación:")
        nombre_facturacion = input("")
        print("RFC:")
        rfc = input("")
        print("Nombre de la persona de contacto:")
        nombre_contacto = input("")
        print("Correo:")
        email_valido = 0
        while email_valido == 0:
            email_constancia = input()

            pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")

            if not re.fullmatch(pattern, email_constancia):
                print("Por favor ingrese una dirección de correo valida.")
            else:
                email_valido = 1
        print("Telefono:")
        Telefono = input()
        print("¿Cómo se enteró de Fibremex?")
        informacion = input("")

    elif respuesta == "otro":
        print("dsd")



    print("hacer cotizacion")
    #print(cotizacion)   #  --> aca ya hay que filtrar el tipo de consuta, si es cotizacion o solo enviar detalles de producto.



	
