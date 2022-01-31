import pyttsx3
import speech_recognition as sr
import time
import sys
import pygame
import config

# import pycaw
#import alsaaudio
#import applescript

# TODO:
#       add reading of ocr text result
#       add interrupt handling and multithreading support
#       for testing purposes, pass in sample text as command line arg
#           i.e. `python tts1.py sampletext.txt`

# references:
#               https://stackoverflow.com/questions/65730317/how-to-pause-resume-and-stop-pyttsx3-from-speaking
#               Using this, we will finish processing the text to speech before beginning reading (for now)
#   https://stackoverflow.com/questions/20828752/python-change-master-application-volume

'''
engine = None
already_processed = None
r = None
m = None
outfile = None
sampleText = "hi hi"
'''

engine = None
r = None
m = None


def init():
    global engine, r, m  
    if sys.platform == "win32":
        pass
        # import pycaw
    elif sys.platform == "darwin":
        import applescript
    elif sys.platform == "linux":
        import alsaaudio
    else:
        print("volume controls not supported")
    pygame.mixer.init()
    engine = pyttsx3.init()
    r = sr.Recognizer()
    m = sr.Microphone()
    calibrate()

def process_text():
    # global config.sampleText
    while config.sampleText == None:
        pass
    global engine
    config.outfile = "temp.wav"
    engine.setProperty('rate', 100)
    engine.save_to_file(config.sampleText, config.outfile)
    engine.runAndWait()

def read():
    global engine, r, m # , config.outfile, config.sampleText
    print('read function')
    if (config.outfile !=  None):
        if not pygame.mixer.music.get_busy(): # don't restart if file is already playing
            try: 
                pygame.mixer.music.load(config.outfile)
                pygame.mixer.music.play()
            except pygame.error as e:
                if e.args[0] is not None:
                    if 'No file' in e.args[0]:
                        print('temp.wav not yet outputted. try again later')
                    else:
                        print(e.message)
                else:
                    print(str(e))

def stop():
    print('stop function')
    pygame.mixer.music.stop()

def pause():
    print('pause function')
    pygame.mixer.music.pause()

def unpause():
    pygame.mixer.music.unpause()

def volumeUp():
    pygame.mixer.get_volume()

def calibrate():
    global r, m
    with m as source: 
        r.adjust_for_ambient_noise(source)

def speech_and_text():
    global engine, r, m
    while (1):
        with sr.Microphone() as source:
            print("say something!")
            time.sleep(1)
            audio = r.listen(source)
        try:
            speech = r.recognize_google(audio)
            print("You said: " + speech)

            speech = speech.split()[0]
            print("Command given: " + speech)

            if speech == "start":
                phrase = "starting text reading"
                read()
            elif speech == "stop":
                phrase = "stopping text reading"
                pause()
            elif speech == "pause":
                phrase = "pausing text reading"
                pause()
            elif speech == "play":
                phrase = "resuming text reading"
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


def main():
    global sample_text, engine, r, m, already_processed
    init()
    sampletextfile = open(sys.argv[1], "r")
    sampleText = sampletextfile.read()
    process_text()
    speech_and_text() 

if __name__=='__main__':
    main()

