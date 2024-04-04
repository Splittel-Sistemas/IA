import random
import json
import pickle
import numpy as np
import re
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

from categorias import*
from saludos import*

lemmatizer = WordNetLemmatizer()

#Importamos los archivos generados en el código anterior
intents = json.loads(open('chatsRaul.json').read())
words = pickle.load(open('words.pkl', 'rb'))

classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('Raul_model.h5')

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



# print('Hola, Soy Raul, ¿Con quién tengo el gusto?')
# user_input = input()
# nombre = user_input
# print(nombre + ', ¿Dónde trabaja?')
# user_input = input()
# trabajo = user_input


# print('¿Me puede proporcionar un correo electrónico por favor?')
# email_valido = 0
# while email_valido == 0:
#     user_input = input()
#     email = user_input

#     pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")

#     if not re.fullmatch(pattern, email):
#         print("Por favor ingrese una dirección de correo valida.")
#     else:
#         email_valido = 1


# print('¿En qué le puedo ayudar ' + nombre +'?')

#Ejecutamos el chat en bucle
while True:
    message=input("")
    ints = predict_class(message.lower())
    if ints == "saludos":
        mensaje, nombre = saludos(ints, intents)
        ints = predict_class(mensaje.lower())
        fin = categoria(ints, intents, mensaje)
    else:
        fin = categoria(ints, intents, message)

    if fin == -1:
        break

    else:
        print("¿Algo más en lo que le pueda ayudar?")

    