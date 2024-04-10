import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import json
import pickle
import random
import ia_cotizaciones
import re
import ia_catalogo
import ia_informacion


def main_ia1(self, text):
  lemmatizer = WordNetLemmatizer()
  intents = json.loads(open('chatsRaul.json').read())
  words = pickle.load(open('words.pkl', 'rb'))

  classes = pickle.load(open('classes.pkl', 'rb'))
  model = load_model('Raul_model.h5')

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



  text_minuscula = text.lower()
  mensaje = text
  opt_ = []
  intern_flow = []
  acciones = []


  clase = predict_class(text_minuscula)
  response = get_response(clase, intents)
  print(clase)
  print(self.saludos)


  
  if (clase == "saludos" or self.saludos == True) and self.inicio == False:

    mensaje = []
    if clase == "saludos" and self.saludos == False:
      mensaje.append(response)
      opt_ = clase
      self.saludos = True
    elif self.saludos == True:
      self.nombre = text
      print("entro")
      self.nombre = re.sub("Con", "", self.nombre)
      self.nombre = re.sub("con", "", self.nombre)
      mensaje.append("En que le puedo ayudar el dia de hoy, " + self.nombre + "?")
      self.saludos = False

  elif (clase == "cotizaciones" or self.cotizaciones == True) and self.catalogo == False:
    self.inicio = True
    mensaje = []
    
    if clase == "cotizaciones":
      acciones = "reaccionSaludo"
      self.cotizaciones = True
      mensaje.append("Antes de continuar, ha comprado anteriormente con nosotros?")
      self.question1 = True

    elif self.cotizaciones == True:
      if self.question2 == True:
        if self.rfc_valido == False:
          rfc = text.upper()
          self.RFC_cliente, self.rfc_valido = verificar_RFC(rfc)
          if self.rfc_valido == True:
            mensaje_, self.question1, self.question2, self.cliente, self.RFC_cliente, self.cotizaciones, self.nContacto, self.correo, self.telefono, self.info, self.correo_val, self.telefono_val, self.giro = self.ia_Cotizacion(text_minuscula, self.question1, self.question2, self.cliente, self.RFC_cliente, self.cotizaciones,self.nContacto, self.correo, self.telefono, self.info, self.correo_val, self.telefono_val, self.giro)
          else:
            mensaje_ = ("Me puede proporcionar un RFC valido, por favor.")
        elif self.rfc_valido == True:
          mensaje_, self.question1, self.question2, self.cliente, self.RFC_cliente, self.cotizaciones, self.nContacto, self.correo, self.telefono, self.info, self.correo_val, self.telefono_val, self.giro = self.ia_Cotizacion(text_minuscula, self.question1, self.question2, self.cliente, self.RFC_cliente, self.cotizaciones,self.nContacto, self.correo, self.telefono, self.info, self.correo_val, self.telefono_val, self.giro)
      else:
        mensaje_, self.question1, self.question2, self.cliente, self.RFC_cliente, self.cotizaciones, self.nContacto, self.correo, self.telefono, self.info, self.correo_val, self.telefono_val, self.giro = self.ia_Cotizacion(text_minuscula, self.question1, self.question2, self.cliente, self.RFC_cliente, self.cotizaciones, self.nContacto, self.correo, self.telefono, self.info, self.correo_val, self.telefono_val, self.giro)
 

      mensaje.append(mensaje_)
      
      if self.cotizaciones == False:
        mensaje.append("Le puedo apoyar con algo mas?")

      
  elif clase == "catalogo" or self.catalogo == True:
    self.inicio = True
    mensaje = []
    if clase == "catalogo":
      acciones = "reaccionSaludo"
      mensaje.append(response)
      mensaje.append("Le compartimos nuestro catalogo digital.")
      mensaje.append("https://publicaciones.fibremex.com/catalogo-telecomunicaciones-fibremex/page/1")
      mensaje.append("Desea que le realicemos alguna cotizacion?")
      acciones = "enviarCatalogo"
      self.catalogo = True

    elif self.catalogo == True:
      mensaje_, self.r_catalogo = ia_catalogo.ia_(text_minuscula)
      if self.r_catalogo == "si":
        self.cotizaciones = True
        self.question1 = True
        self.catalogo = False
        mensaje.append("Antes de continuar, ha comprado anteriormente con nosotros?")
        
      elif self.r_catalogo == "no":
        mensaje.append(mensaje_)
        mensaje.append("Le puedo apoyar con algo mas?")
        self.catalogo = False

      else:
        mensaje.append(mensaje_)
        mensaje.append("Me lo puede repetir de otra manera por favor.")
    
  elif clase == "informacion_cursos":
    self.inicio = True
    acciones = "reaccionSaludo"
    mensaje = []
    mensaje.append(response)
    mensaje.append("Puede consultar nuestros seminarios online gratuitos en el siguiente link:")   #hacer consulta
    mensaje.append("https://fibremex.com/fibra-optica/views/Capacitaciones/2-seminarios-online")
    mensaje.append("Para incribirse a cualquiera de nuestros seminarios online solo debe llenar el formato que se encuentra en el link que le proporcione.")
    mensaje.append("Puede consultar nuestros cursos presenciales en el siguiente link:")
    mensaje.append("https://fibremex.com/fibra-optica/views/Capacitaciones/3-cursos-presenciales-fibra-optica")
    mensaje.append("Para inscribirse a cualquiera de nuestros cursos presenciales debe llenar los datos requeridos en el link proporicionado,")
    mensaje.append("Posteriormente, un asesor se pondrá en contacto con usted para darle mas detalles de la inscripción.")
    mensaje.append("*Todos los cursos presenciales son impartidos en la ciudad de Queretaro.")
    mensaje.append("Le puedo apoyar con algo mas?")
    
  elif clase == "cursos_seminarios_constancias" or self.email == True:
    self.inicio = True
    mensaje = []
    if clase == "cursos_seminarios_constancias":
      acciones = "reaccionSaludo"
      mensaje.append(response)
      self.email = True
      
    elif self.email == True:
      self.email_constancia = text
      pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")

      if not re.fullmatch(pattern, self.email_constancia):
        mensaje.append("Me puede proporcionar un correo valido por favor.")
      else:
        self.email = False
        mensaje.append("En un momento le enviaremos su constancia al correo: " + str(self.email_constancia)) 
        mensaje.append("Por favor revise su bandeja de SPAM.")
        mensaje.append("Le puedo apoyar con algo mas?")


  elif clase == "facturacion" or self.factura == True:
    self.inicio = True
    mensaje = []

    if clase == "facturacion":
      acciones = "reaccionSaludo"
      mensaje.append(response)
      mensaje.append("Me puede indicar su RFC por favor.")
      self.factura = True

    elif self.factura == True:
      rfc = text
      self.RFC_cliente, self.rfc_valido = verificar_RFC(rfc)
      if self.rfc_valido == True:
        mensaje.append("Gracias!")
        mensaje.append("En un momento su ejecutivo de ventas se pondrá en contacto con usted para enviarle la información solicitada.")
        mensaje.append("Le puedo apoyar con algo mas?")
        self.factura = False
      else:
        mensaje.append("Me puede brindar un RFC valido, por favor.")


  elif clase == "problemas_acceso" or self.acceso == True:
    self.inicio = True
    mensaje = []

    if clase == "problemas_acceso":
      acciones = "reaccionSaludo"
      mensaje.append("Para los problemas relaccionados al acceso a su cuenta es necesario transferirlo con otro ejecutivo.")
      mensaje.append(response)
      self.acceso = True

    elif self.acceso == True:
      rfc = text
      self.RFC_cliente, self.rfc_valido = verificar_RFC(rfc)
      if self.rfc_valido == True:
        mensaje.append("En unos momentos otro ejecutivo se pondra en contacto con usted para solucionar sus problemas de acceso.")
        mensaje.append("Le puedo apoyar con algo mas?")
        self.acceso = False
      else:
        mensaje.append("Me puede proporcionar un RFC valido, por favor.")

  elif clase == "servicios" or self.servicio == True:
    self.inicio = True
    mensaje = []

    if clase == "servicios":
      acciones = "reaccionSaludo"
      mensaje.append(response)
      mensaje.append("Me puede apoyar con su RFC por favor.")
      self.servicio = True
    elif self.servicio == True:
      rfc = text
      self.RFC_cliente, self.rfc_valido = verificar_RFC(rfc)
      if self.rfc_valido == True:
        mensaje.append("Este es el contacto de su ejecutivo de ventas:")
        mensaje.append("En un momento su ejecutivo de ventas se pondrá en contacto con usted para atenderlo.")
        mensaje.append("Le puedo apoyar con algo mas?")
        acciones = "enviarContacto"
        self.servicio = False
      else:
        mensaje.append("Me puede proporcionar un RFC valido, por favor.")


  elif clase == "estatusPedido" or self.estatus == True:
    self.inicio = True
    mensaje = []
    if clase == "estatusPedido":
      acciones = "reaccionSaludo"
      mensaje.append(response)
      mensaje.append("Me puede apoyar con los siguientes datos por favor.")
      mensaje.append("Número de pedido:")
      self.estatus = True
      

    elif self.estatus == True and self.numeroPedido == []:
      mensaje.append("Número de teléfono:")
      self.numeroPedido = text

    elif self.numeroPedido != [] or self.telefono_val == False:
      self.telefono = text
      if len(self.telefono) == 10 and self.telefono.isdigit():
        self.telefono_val = True
        self.estatus = False
        mensaje.append("Muchas gracias! en un momento su ejecutivo de ventas se estará comunicando con usted para brindarle más información acerca de su pedido.")
        mensaje.append("Por el momento, este es su número de guia por si desea rastrear su pedido.")
        mensaje.append("Le puedo apoyar con algo mas?")
      else:
        mensaje.append("Me puede brindar un número de teléfono valido, por favor.")
    

  elif clase == "puntos_ventas_envios":
    self.inicio = True
    acciones = "reaccionSaludo"
    mensaje = []
    mensaje.append(response)
    mensaje.append("Nuestro punto de ventas fisico se encuetra en:")
    mensaje.append("Parque Tecnológico Innovación Querétaro, Lateral de la carretera Estatal 431, km.2+200, Int.28, C.P.76246")
    mensaje.append("Contamos con envio a toda la Republica Mexicana.")
    mensaje.append("También contamos con envios internacionales.")
    mensaje.append("Le puedo apoyar con algo mas?")
    acciones = "enviarUbicacion"

  elif clase == "informacion_perdida" or self.informacionPerdida == True:
    self.inicio = True
    mensaje = []

    if clase == "informacion_perdida" and self.informacionPerdida == False:
      self.informacionPerdida = True
      mensaje.append(response)
      mensaje.append("Le llego la información?")
      #llamar a funcion para si o no

    elif self.informacionPerdida == True:
      respuesta = self.ia_Info(text_minuscula)
      print(respuesta)
      print(self.respuesta)

      if respuesta == "si" and self.respuesta == False:
        mensaje.append("Le puedo ayudar con algo mas?")
        self.informacionPerdida = False

      elif respuesta == "no" and self.respuesta == False:
        mensaje.append("Una disculpa por las molestias que esto le pueda ocasionar.")
        mensaje.append("Me puede apoyar con su RFC por favor? para enviarle la información solicitada lo antes posible.")
        self.respuesta = True

      elif respuesta == "espera" and self.respuesta == False:
        mensaje.append("Ok.")

      elif self.rfc_valido == False:
        rfc = text
        self.RFC_cliente, self.rfc_valido = verificar_RFC(rfc)
        if self.rfc_valido == True:
          mensaje.append("Gracias.")
          mensaje.append("Le enviaremos la información lo antes posible.")
          mensaje.append("Le puedo ayudar con algo mas?")
          self.informacionPerdida = False
        else:
          mensaje.append("Me puede proporcionar un RFC valido por favor.")

  elif clase == "badWords":
    self.inicio = True
    mensaje = []
    mensaje.append(response)
  
  elif clase == "final":
    #acciones = "reaccionSaludo"
    mensaje = []
    mensaje.append(response)
    self.vIniciales()
    self.fin = True
    
  
  
  return mensaje, acciones

def conversacion_ia1(self, text, number):
  self.conversacion.append(text)
  if self.fin == True:
    np.savetxt("conversacion"+str(number)+".txt", self.conversacion, fmt="%s", delimiter=",")
    self.fin = False

def verificar_RFC(rfc):
  rfc_ = rfc.upper()
  rfc_valido = False
  if len(rfc_) == 12 or len(rfc_) == 13:
    if len(rfc_) == 12:
      letras = rfc_[:3]
      numeros = rfc_[3:9]
      
    else:
      letras = rfc_[:4]
      numeros = rfc_[4:10]
      

    if letras.isalpha() and numeros.isdigit():
      rfc_valido = True

    else:
      rfc_valido = False

  else:
    rfc_valido = False

  print(rfc_valido)
  return rfc_, rfc_valido

  
def vIniciales1( self ):
  self.inicio = False  

  self.saludos = False
  self.cotizaciones = False
  self.fin = False
  self.conversacion = []
  self.nombre = []

  self.cliente = False
  self.question1 = False
  self.question2 = False
  self.RFC_cliente = []
  self.nContacto = []
  self.correo = []
  self.telefono = []
  self.info = []
  self.correo_val = False
  self.telefono_val = False
  self.giro = []

  self.email = False
  self.email_constancia = []
  self.factura = False

  self.acceso = False
  self.servicio = False
  self.catalogo = False
  self.r_catalogo = []

  self.estatus = False
  self.numeroPedido = []

  #RFC validacion
  self.rfc_valido = False

  self.informacionPerdida = False
  self.respuesta = False

class d_flow:
    vIniciales = vIniciales1
    main_ia = main_ia1
    conversacion_ia = conversacion_ia1

    ia_Cotizacion = ia_cotizaciones.ia_
    ia_Info = ia_informacion.ia_
