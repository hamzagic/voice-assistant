import serial
import threading
import time
import speech_recognition as sr 
import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')
count = 0
for voice in voices:
   # print(count, voice) 
   # voice 22 is the only pt-BR
    count += 1

voice = 22
engine.setProperty('voice', voices[voice].id)

r = sr.Recognizer()
mic = sr.Microphone()

connected = False
port = '/dev/cu.usbmodem14201'
baud = 9600

msgCount = 0
turnOffThread = False

speakText = False
receivedText = ""

try:
    SerialArduino = serial.Serial(port, baud, timeout = 0.2)
except:
    print("***Verify port or turn on Arduino***")

def handle_data(data):
    global msgCount, engine, speakText, receivedText
    print("Received " + str(msgCount) + ":" + data)
    msgCount += 1
    receivedText = data
    speakText = True
    

def read_from_port(ser):
    global connected, turnOffThread

    while not connected:
        connected = True

        while True:
            reading = ser.readline().decode()
            if reading != "":
                handle_data(reading)
            if turnOffThread:
                print("Turning off Arduino connection")
                break

readSerialThread = threading.Thread(target=read_from_port, args=SerialArduino)
readSerialThread.start()

print("Preparing Arduino...")
time.sleep(3)
print("Arduino ready")

while (True):
    if speakText:
        #not working, need to check
        engine.say(receivedText)
        engine.runAndWait()

        speakText = False
    
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            print("Envie seu comando de voz")
            audio = r.listen(source)
            print("Enviando...")
        try:
            text = r.recognize_google(audio, language='pt-BR').lower()
            print("Voce disse: {0}".format(text))
            if (text == 'vermelho' or text == 'amarelo' or text == 'verde'):
                try:
                    engine.say("ligar" + text)
                    engine.say("bruno é besta")
                    engine.runAndWait()
                except:
                    print("Sem socket")
            SerialArduino.write((text + '\n').encode())

            print("Dado enviado")
            if(text == 'desativar'):
                print("Desligando...")
                turnOffMsg = "Assistente desligando"

                engine.say(turnOffMsg)
                engine.runAndWait()
                engine.stop()

                turnOffThread = True
                SerialArduino.close()
                readSerialThread.join()
                break
        except:
            print("Nao entendi")
        time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Ctrl+C activated")
        turnOffThread = True
        SerialArduino.close()
        readSerialThread.join()
        break
   