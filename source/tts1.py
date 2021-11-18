import pyttsx3
import speech_recognition as sr
import time
import sys
import pygame
import threading

# TODO:
#       add reading of ocr text result
#       add interrupt handling and multithreading support
#       for testing purposes, pass in sample text as command line arg
#           i.e. `python tts1.py sampletext.txt`

sampletextfile = open(sys.argv[1], "r")
sampletext = sampletextfile.read()

engine = pyttsx3.init()
r = sr.Recognizer()
m = sr.Microphone()
with m as source: r.adjust_for_ambient_noise(source)

engine.say(sampletext)
engine.runAndWait()
while (1):
    with sr.Microphone() as source:
        print("say something!")
        time.sleep(1)
        audio = r.listen(source)
    try:
        speech = r.recognize_google(audio)
        print("You said: " + speech)

        if speech == "start":
            phrase = "starting text reading"
            engine.say(phrase)
            print(phrase)
        elif speech == "stop":
            phrase = "stopping text reading"
            engine.say(phrase)
            print(phrase)
        elif speech == "speed up":
            phrase = "speeding up"
            engine.say(phrase)
            print(phrase)
        elif speech == ("slow down"):
            phrase = "slowing down"
            engine.say(phrase)
            print(phrase)

        elif speech == "hello":
            engine.say("Hi there. Welcome to Read Me.")
        engine.runAndWait()

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Error; {0}".format(e))

