import speech_recognition as sr 

r = sr.Recognizer()
mic = sr.Microphone()
with mic as src:
    r.adjust_for_ambient_noise(src)
    print("Diga algo")
    audio = r.listen(src)
    print("Enviando...")

try:
   text = r.recognize_google(audio, language="pt-BR")
   print("Voce disse: {0}".format(text))
except:
    print("Nao entendi")