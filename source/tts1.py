import pyttsx3
import speech_recognition as sr
import time
import sys
import pygame

# TODO:
#       add reading of ocr text result
#       add interrupt handling and multithreading support
#       for testing purposes, pass in sample text as command line arg
#           i.e. `python tts1.py sampletext.txt`

# references:
#		https://stackoverflow.com/questions/65730317/how-to-pause-resume-and-stop-pyttsx3-from-speaking
#		Using this, we will finish processing the text to speech before beginning reading

sampletextfile = open(sys.argv[1], "r")
sampleText = sampletextfile.read()

pygame.mixer.init()
engine = pyttsx3.init()
r = sr.Recognizer()
m = sr.Microphone()

already_processed = False

def read():
	outfile = "temp.wav"
	if not already_processed:
		engine.save_to_file(sampleText, outfile)
		engine.runAndWait()
	pygame.mixer.music.load(outfile)
	pygame.mixer.music.play()

def stop():
    pygame.mixer.music.stop()

def pause():
    pygame.mixer.music.pause()

def unpause():
    pygame.mixer.music.unpause()

with m as source: 
	r.adjust_for_ambient_noise(source)

while (1):
    with sr.Microphone() as source:
        print("say something!")
        time.sleep(1)
        audio = r.listen(source)
    try:
        speech = r.recognize_google(audio)
        print("You said: " + speech)

        speech = speech.split()[0]
        print("Command given: " speech)

        if speech == "start":
            phrase = "starting text reading"
            print(phrase)
            read()
        elif speech == "stop":
            phrase = "stopping text reading"
            print(phrase)
            pause()
        elif speech == "pause":
            phrase = "pausing text reading"
            print(phrase)
            pause()
        elif speech == "play":
            phrase = "resuming text reading"
            print(phrase)
            unpause()
	    # TODO speeding up/down currently not implemented, 
	    #      complications with the time required to resample the wav file
            '''
            elif speech == "speed up":
                phrase = "speeding up"
                engine.say(phrase)
                print(phrase)
            elif speech == ("slow down"):
                phrase = "slowing down"
                engine.say(phrase)
                print(phrase)
            '''

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Error; {0}".format(e))

