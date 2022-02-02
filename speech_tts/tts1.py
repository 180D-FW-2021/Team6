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

# https://stackoverflow.com/questions/58630700/utilising-the-pygame-mixer-music-get-endevent

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
screen = None
count = 0
play_count = 0
MUSIC_END = pygame.USEREVENT+1
started = False
paused = False

def init():
    global engine, r, m, screen  
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
    # screen = pygame.display.set_mode((1, 1))
    engine = pyttsx3.init()
    r = sr.Recognizer()
    m = sr.Microphone(device_index=0)
    calibrate()

def process_text():
    # global config.sampleText
    while config.sampleText == None:
        pass
    global engine, count
    config.outfile.append("temp%s.wav" % str(count))
    engine.setProperty('rate', 100)
    engine.save_to_file(config.sampleText[count], config.outfile[count])
    engine.runAndWait()
    count += 1

def read():
    global engine, r, m, play_count, count, started, paused # , config.outfile, config.sampleText
    print('read function')
    if len(config.outfile) > 0 and play_count < count:
        if not pygame.mixer.music.get_busy(): # don't restart if file is already playing
            try:
                print(play_count, count)
                pygame.mixer.music.load(config.outfile[play_count])
                pygame.mixer.music.play()
                started = True
                paused = False
                # pygame.mixer.music.set_endevent(MUSIC_END)
            except pygame.error as e:
                if e.args[0] is not None:
                    if 'No file' in e.args[0]:
                        print('temp.wav not yet outputted. try again later')
                    else:
                        print(e.message)
                else:
                    print(str(e))

def stop():
    global started, paused
    print('stop function')
    started = False
    paused = True
    pygame.mixer.music.stop()


def pause():
    global started, paused
    print('pause function')
    paused = True
    pygame.mixer.music.pause()

def unpause():
    global started, paused
    paused = False
    pygame.mixer.music.unpause()

def volumeUp():
    pygame.mixer.get_volume()

def calibrate():
    global r, m
    with m as source: 
        r.adjust_for_ambient_noise(source)

def speech():
    global engine, r, m, MUSIC_END, play_count, started, paused
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
                # pygame.mixer.music.set_endevent(MUSIC_END)
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


def tts():
    global engine, r, m, MUSIC_END, play_count, started, paused
    while (1):
        try:
            '''
            for event in pygame.event.get():
                if event.type == MUSIC_END:
                    print('music end event')
                    #if pygame.mixer.music.get_endevent():
                    #    print('music end event')
                    play_count += 1
                    pygame.mixer.music.set_endevent()
            '''
            '''
            if pygame.mixer.music.get_endevent():
                print('music end event')
                play_count += 1
                # pygame.mixer.music.set_endevent()
            '''
            pass
        except pygame.error as e:
            print(e.args[0])
        if started and not paused and not pygame.mixer.music.get_busy():
            started = False
            print( 'music end' )
            play_count +=1


def main():
    global sample_text, engine, r, m, already_processed
    init()
    sampletextfile = open(sys.argv[1], "r")
    sampleText = sampletextfile.read()
    process_text()
    speech_and_text() 

if __name__=='__main__':
    main()

