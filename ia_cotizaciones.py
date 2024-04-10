import random
import json
import pickle
import numpy as np
import re
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model


def ia_(self, mensaje_inicial, question1, question2, cliente, RFC_cliente, cotizaciones, nContacto, correo, telefono, info, correo_val, telefono_val, giro):
    #self.prueba = False
   # print(self.prueba)
    lemmatizer = WordNetLemmatizer()
    #Importamos los archivos generados en el código anterior
    intents = json.loads(open('cotizaciones.json').read())
    words = pickle.load(open('words_cotizaciones.pkl', 'rb'))
    classes = pickle.load(open('classes_cotizaciones.pkl', 'rb'))
    model = load_model('cotizaciones_model.h5')

    mensaje_ = mensaje_inicial
    question1_ = question1
    question2_ = question2
    cliente_ = cliente
    RFC_cliente_ = RFC_cliente
    cotizaciones_ = cotizaciones
    nContacto_ = nContacto
    correo_ = correo
    telefono_ = telefono
    info_ = info
    telefono_val_ = telefono_val
    correo_val_ = correo_val
    giro_ = giro

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


    if question1 == True and question2 == False:   
        #if RFC_cliente == []:
        respuesta = predict_class(mensaje_inicial)

        if respuesta == "si":
            mensaje_ = "Gracias por consideranos nuevamene, me puede proporcionar su RFC por favor."
            question2_ = True
            cliente_ = True
        elif respuesta == "no":
            mensaje_ = "Para brindarle un mejor servicio y ponerlo en contacto con un ejecutivo de ventas, me podria brindar los siguientes datos por favor!\nRFC:"
            question2_ = True
            cliente_ = False
        else:
            mensaje_ = "Una disculpa, no entiendo su respuesta, me lo puede decir de otra manera por favor."
        # elif RFC_cliente != [] and self.preguntaRFC == False:
        #     mensaje.append("Desea que utilicemos este RFC: " + str(RFC_cliente) + "?")
        #     self.preguntaRFC = True

        # elif self.preguntaRFC == True:
        #     respuesta = predict_class(mensaje_inicial)

        #     if respuesta == "si":
        #         mensaje.append("Perfecto.")
        #         question2_ = True
        #         cliente_ = True

        #     elif respuesta == "no":
        #         mensaje.append("Por favor ingrese el nuevo RFC:")
        #         question2_ = True
        #         cliente_ = True

        #     else:
        #         mensaje.append("No entendi su respuesta")


    elif question2 == True and cliente == True:
    
        RFC_cliente_ = mensaje_inicial
        mensaje_ = "Confirmar datos"
        question2_ = False
        cotizaciones_ = False

    elif question2 == True and cliente == False:
        if RFC_cliente == []:
            RFC_cliente_ = mensaje_inicial
            mensaje_ = "Nombre de Contacto:"

        elif nContacto == []:
            nContacto_ = mensaje_inicial
            correo_val_ = False
            mensaje_ = "Correo Electronico:"

        elif correo_val == False:
            correo_ = mensaje_inicial
            pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")

            if not re.fullmatch(pattern, correo_):
                mensaje_ = ("Me puede proporcionar un correo valido por favor.")
            else:
                correo_val_ = True
                mensaje_ = ("Número de Teléfono:")
                telefono_val_ = False

        elif telefono == [] or telefono_val == False:
            telefono_ = mensaje_inicial
            if len(telefono_) == 10 and telefono_.isdigit():
                telefono_val_ = True
                mensaje_ = ("Cuál es el giro de la empresa (Indicar que actividades realiza dentro del Giro).")
                
            else:
                mensaje_ = ("Me puede dar un teléfono válido por favor.")

        elif giro == []:
            giro_ = mensaje_inicial
            mensaje_ = ("Cómo se enteró de Fibremex?")

        elif info == []:
            info_ = mensaje_inicial
            question2_ = False
            cotizaciones_ = False
            mensaje_ = ("Me puede indicar por favor el o los productos que desea cotizar, seguido de la cantidad. Por ejemplo:\nGabinete OPGAPIMG042OSH - 2 unidades")
        

    return mensaje_, question1_, question2_, cliente_, RFC_cliente_, cotizaciones_, nContacto_, correo_, telefono_, info_, correo_val_, telefono_val_, giro_


