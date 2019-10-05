import pyttsx3

engine = pyttsx3.init()
engine.say("Get out")
engine.runAndWait()
engine.stop()