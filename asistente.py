import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes as jk
import yfinance as yf
import webbrowser
import os
import openai
import pyaudio
import unicodedata


#clave de openai
openai.api_key = os.getenv('')


#escuchar y devolver un texto
def Transcribe_audio_to_text():

    #almacenar el audio
    r = sr.Recognizer()

    #configurar el microfono
    with sr.Microphone() as source:  
    
        #tiempo de espera para escuchar la voz
        r.pause_threshold = 0.8 

        #informar que comenzo a escuchar
        print("Ya puedes comenzar a hablar...")

        #almacenar el audio
        audio = r.listen(source) 

        try:
            #buscar en google lo que se dijo
            order = r.recognize_google(audio, language='es-ES')

            #imprimir lo que se dijo
            print("Tu dijiste: " + order)

            #devolver lo que se dijo
            return order

        #si no se entiende lo que se dijo
        except sr.UnknownValueError:

            #imprimir que no se entiende
            print("lo siento, no te entendi")

            #devolver error
            return "repiteme por favor"

        #en caso de no resolver el pedido
        except sr.RequestError:

            #imprimir que el pedido no se resolvio
            print("lo siento, parece que tu pedido es muy complicado para mi")

            #devolver error
            return "pideme otra cosa, por favor"
        
        #error general
        except:

            #imprimir que algo salio mal
            print("lo siento, algo salio mal")

            #devolver error
            return "pideme otra cosa, por favor"


#funcion para integrar openai
def answer_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message['content']


#funcion para que el asistente hable 
def Speak(text):

    #encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    #pronunciar el texto
    engine.say(text)
    engine.runAndWait()

#funcion para eliminar acentos
def remove_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')


#voz del asistente 'sabina'
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'


#decir el dia actual
def ask_for_day():
    
    day = datetime.date.today()
    print(day)
        
    week_day = day.weekday()
    print(week_day)

    calendary = {0: 'Lunes',  
                 1: 'Martes',
                 2: 'Miercoles',
                 3: 'Jueves',
                 4: 'Viernes', 
                 5: 'Sabado', 
                 6: 'Domingo'}

    Speak(f"Hoy es {calendary[week_day]}")


#decir la hora
def ask_for_time():
    
    time = datetime.datetime.now().strftime('%I:%M %p')
    print(time)
    
    Speak(f"Son las {time}")


#funcion de saludo inicial
def first_message():

    time = datetime.datetime.now()

    if time.hour >= 18:
        time = "Buenas noches"
    
    elif time.hour >= 12:
        time = "Buenas tardes"
    
    else:
        time = "Buenos dias"

    Speak(f"{time}, Mi nombre es sabina y soy tu asistente personal, ¿en que puedo ayudarte?")


#pedir cosas
def questions():

    #activar el saludo inical
    first_message()

    #variable de inicio 
    start = True

    #loop para escuchar pedidos
    while start:

        #escuchar el pedido
        order = Transcribe_audio_to_text().lower()
        order = remove_accents(order)

        #solamente abre youtube sin buscar nada
        if 'abrir youtube' in order:

            Speak("Abriendo youtube")
            webbrowser.open("https://www.youtube.com/")
            continue

        #solamente abre google sin buscar nada
        elif 'abrir google' in order:

            Speak("Abriendo google")
            webbrowser.open("https://www.google.com/")
            continue

        #abre el gmail
        elif 'abrir gmail' in order:

            Speak("Abriendo gmail")
            webbrowser.open("https://www.gmail.com/")
            continue
        
        #indica que dia es hoy
        elif 'dia es hoy' in order:

            ask_for_day()
            continue
        
        #indica que hora es
        elif 'que hora es' in order:

            ask_for_time()
            continue

        #busca en wikipedia lo que el usuario pide
        elif 'busca en wikipedia' in order:
            
            for word in ['busca en wikipedia', 'por favor', 'hola', 'sabina']:
                order = order.replace(word, "")
            wikipedia.set_lang("es")
            result = wikipedia.summary(order, sentences=1)
            Speak(f"wikipedia dice que {result}")
            continue
        
        #busca en google lo que el usuario pide
        elif 'busca en google' in order:

            for word in ['busca en google', 'por favor', 'hola', 'sabina']:
                order.replace(word, "")
            webbrowser.open(f"https://www.google.com/search?q={order}") 
            continue

        #reproduce musica en youtube
        elif 'reproducir' in order:

            Speak('ya comienzo a reproducirlo')
            pywhatkit.playonyt(order)

        #cuenta un chiste
        elif 'chiste' in order:

            Speak(jk.get_joke('es'))
            continue

        #indica el precio de una accion y su disponibilidad
        elif 'acciones' in order:

            market = order.split('de') [-1].strip()
            stock = {'apple': 'AAPL',
                     'amazon': 'AMZN',
                     'google': 'GOOGL', 
                     'microsoft': 'MSFT', 
                     'tesla': 'TSLA'}
            try: 
                market_search = stock[market]
                market_search = yf.Ticker(market_search)
                price = market_search.info['regularMarketPrice']
                Speak(f"El precio de {market} es de {price} dolares")
                continue
            except:
                Speak("No pude encontrar la informacion que buscas")
                continue

        #chat con gpt
        elif 'chat gpt' in order:
            
            Speak("¿Qué quieres preguntarme?")
            user_question = Transcribe_audio_to_text()
            response = answer_openai(user_question)
            Speak(response)
            continue

        #despedida
        elif 'adios' in order:

            time = datetime.datetime.now()

            if time.hour >= 18:
                time = "Buena noche"
    
            elif time.hour >= 12:
                time = "Buena tarde"
    
            else:
                time = "Buen dia"

            Speak(f"que tengas {time}, espero haberte ayudado, hasta luego")
        
            break

questions()

