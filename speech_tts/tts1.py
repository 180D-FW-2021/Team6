import pyttsx3
import speech_recognition as sr
import time
import sys
import pygame
import config

from multiprocessing import Queue
from queue import Empty

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


MUSIC_END = pygame.USEREVENT+1

def init():
    global engine, r, m, screen 
    pygame.mixer.init()
    engine = pyttsx3.init()
    r = sr.Recognizer()
    m = sr.Microphone(device_index=0)
    calibrate(r,m)
    return engine, r, m

def process_text(textqueue, audioqueue):
    engine = pyttsx3.init()
    count = 0
    outfile = []
    while 1:
        try:
            sampleText = textqueue.get()
            print("hi from process_text", sampleText)
        except Empty as e:
            pass
        else:
            config.gotImage=0
            outfile.append("temp%s.wav" % str(count))
            engine.setProperty('rate', 120)
            engine.save_to_file(sampleText, outfile[count])
            engine.runAndWait()
            audioqueue.put(outfile[count])
            count += 1
            print(count)

def read(audioqueue, started, paused, play_count):
    if not pygame.mixer.music.get_busy():
        if config.started and config.paused:
            paused = False
            pygame.mixer.music.unpause()
        else:
            try:
                aud = audioqueue.get()
                play_count += 1
            except Empty as e:
                print('no audio files yet')
            else:
                pygame.mixer.music.load(aud)
                pygame.mixer.music.play()
                config.started = True
                config.paused = False
    return started, paused, play_count


def stop(started, paused):
    print('stop function')
    config.started = False
    config.paused = False 
    pygame.mixer.music.stop()


def pause(started, paused):
    print('pause function')
    config.paused = True
    pygame.mixer.music.pause()

# might not need this anymore TODO
def unpause(started, paused):
    paused = False
    pygame.mixer.music.unpause()

def volumeUp():
    cur_vol = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(cur_vol + 0.2)

def volumeDown():
    cur_vol = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(cur_vol - 0.2)

def calibrate(r, m):
    with m as source: 
        r.adjust_for_ambient_noise(source)

def speech(commandsqueue, speechbutton2):
    r = sr.Recognizer()
    unpause_after = None
    while (1):
        val = speechbutton2.recv()
        if val == 1:
            unpause_after = True
            commandsqueue.put('pause')
            with sr.Microphone() as source:
                print("say something!")
                # time.sleep(1)
                audio = r.listen(source)
            try:
                speech = r.recognize_google(audio)
                print("You said: " + speech)

                speech = speech.split()[0:2]

                if "play" in speech:
                    commandsqueue.put('start')
                    unpause_after = False
                    # pygame.mixer.music.set_endevent(MUSIC_END)
                elif "stop" in speech:
                    commandsqueue.put('stop')
                    unpause_after = False
                elif "pause" in speech:
                    commandsqueue.put('pause')
                    unpause_after = False
                elif "volume" in speech:
                    if "up" in speech:
                        commandsqueue.put('louder')
                        unpause_after = True
                    if 'down' in speech:
                        commandsqueue.put('softer')
                        unpause_after = True

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
        elif val == 0 and unpause_after:
            commandsqueue.put('start')




def tts(commandsqueue, audioqueue, tts_ui_conn):
    started = False
    paused = False
    play_count = 0
    init()
    while (1):
        try:
            cmd = commandsqueue.get()
            print(cmd, config.started, config.paused)
            if cmd == 'start':
                read(audioqueue, started, paused, play_count)
            elif cmd == 'stop':
                stop(started, paused)
            elif cmd == 'pause':
                pause(started, paused)
            elif cmd == 'louder':
                volumeUp()
            elif cmd == 'softer':
                volumeDown()
           
        except Empty as e:
            pass

        except pygame.error as e:
            pass

        if config.started and not config.paused and not pygame.mixer.music.get_busy():
            config.started = False
            print( 'music end' )
            # play_count +=1


def tts_wrapper(commandsqueue, textqueue):
    while(1):
        pass

def main():
    global sample_text
    engine, r, m = init()
    sampletextfile = open(sys.argv[1], "r")
    sampleText = sampletextfile.read()
    process_text(engine)
    # run speech and tts

if __name__=='__main__':
    main()

