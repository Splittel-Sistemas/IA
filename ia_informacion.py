import random
import json
import pickle
import numpy as np
import re

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model


def ia_(self, mensaje_inicial):
	
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
	

	respuesta = predict_class(mensaje_inicial)

	return respuesta