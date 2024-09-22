import speech_recognition as sr
import playsound 
from gtts import gTTS, tts
import random
import webbrowser
import pyttsx3
import pywhatkit
import datetime
import os
audio = sr.Recognizer()
n=1

class Virtual_assit():
    def __init__(self, assist_name, person):
        self.person = person
        self.assit_name = assist_name

        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        
        self.voice_data = ''

    def engine_speak(self, text):
        """
        fala da assitente virtual
        """
        text = str(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def record_audio(self, ask=""):


        with sr.Microphone() as source:
            if ask:
                if n == 1:
                    ask = f"Olá {self.person}, no que posso ajudar hoje?"
                print('Ouvindo...')
                self.engine_speak(ask)

            audio = self.r.listen(source,5 , 5)# pega dados de auido
            print('olhando para a base de dados')
            try:
                self.voice_data = self.r.recognize_google(audio, language="pt-BR") #converte audio para texto

            except sr.UnknownValueError:
                self.engine_speak('Desculpe, eu não entendi o que você disse. Pode repetir?')

            except sr.RequestError:
                self.engine_speak('Desculpe, meu servidor está inativo') # recognizer is not connected

            print(">>",self.voice_data.lower()) #imprime o que vc disse
            self.voice_data = self.voice_data.lower()

            return self.voice_data.lower()

    def engine_speak(self, audio_strig):
        audio_strig = str(audio_strig)
        tts = gTTS(text=audio_strig, lang='pt-BR')
        r = random.randint(1,20000)
        audio_file = 'audio' + str(r) + '.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(self.assit_name + ':', audio_strig)
        os.remove(audio_file)


    def there_exist(self, terms):
        """
        função para identificar se o termo existe
        """
        for term in terms:
            if term in self.voice_data:
                return True


    def respond(self, voice_data):
        if self.there_exist(['hey', 'oi', 'olá', 'hi', 'holla']):
            greetigns = [f'Olá {self.person}, o que está fazendo hoje?',
                        f'Oi {self.person}, como posso ajudá-lo?',
                        f'Oi {self.person}, o que você precisa?']

            greet = greetigns[random.randint(0,len(greetigns)-1)]
            self.engine_speak(greet)
        if self.there_exist(["bom dia",'boa tarde','boa noite']):
            hora = datetime.datetime.now().strftime('%H')
            hora = int(hora)
            if hora < 12:
                bom = f"bom dia {self.person}, como você está?"
            elif hora >=12 and hora <=18:
                bom = f"boa tarde {self.person}, como você está?"
            else:
                bom = f"boa noite {self.person}, como você está?"
            self.engine_speak(bom)

        #google
        if self.there_exist(['procure por']) and 'youtube' not in voice_data:
            search_term = voice_data.split("por")[-1]
            url =  "http://google.com/search?q=" + search_term
            webbrowser.get().open(url)
            self.engine_speak("aqui está o que eu encontrei para " + search_term + ' em google')

        #google 
        if self.there_exist(["toque", 'tocar']):
            search_term  = voice_data.split("por")[-1]
            musica = search_term.replace('toque','')
            resultado = pywhatkit.playonyt(musica)
            self.engine_speak("aqui está o que eu encontrei para" + search_term + ' em youtube')
            
        
        #horas
        if self.there_exist(["horas"]):
            hora = datetime.datetime.now().strftime('%H:%M')
            self.engine_speak("Agora são " + hora )
        


assistent = Virtual_assit('Ive', 'Valentim')

while True:

    voice_data = assistent.record_audio('Ouvindo...')
    assistent.respond(voice_data)
    n=0

    if assistent.there_exist(['tchau', 'adeus', 'Vejo você depois', 'até mais']):
        hora = datetime.datetime.now().strftime('%H')
        hora = int(hora)
        if hora < 12:
            dia = "um bom dia"
        elif hora >=12 and hora <=18:
            dia = "uma boa tarde"
        else:
            dia = "uma boa noite"
        assistent.engine_speak(f"Tenha {dia}! Até logo!")
        break

