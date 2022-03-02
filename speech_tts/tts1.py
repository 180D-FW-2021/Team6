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

'''
engine = None
already_processed = None
r = None
m = None
outfile = None
sampleText = "hi hi"
'''

MUSIC_END = pygame.USEREVENT+1

def init():
    global engine, r, m, screen 
    ''' 
    if sys.platform == "win32":
        pass
        # import pycaw
    elif sys.platform == "darwin":
        import applescript
    elif sys.platform == "linux":
        import alsaaudio
    else:
        print("volume controls not supported")
    '''
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
    '''
    if len(config.outfile) > 0 and config.play_count < config.count:
        if not pygame.mixer.music.get_busy(): # don't restart if file is already playing
            try:
                print(config.play_count, config.count)
                pygame.mixer.music.load(config.outfile[config.play_count])
                pygame.mixer.music.play()
                config.started = True
                config.paused = False
                # pygame.mixer.music.set_endevent(MUSIC_END)
            except pygame.error as e:
                if e.args[0] is not None:
                    if 'No file' in e.args[0]:
                        print('temp.wav not yet outputted. try again later')
                    else:
                        print(e.message)
                else:
                    print(str(e))
    '''
    if not pygame.mixer.music.get_busy():
        try:
            aud = audioqueue.get()
            play_count += 1
        except Empty as e:
            print('no audio files yet')
        else:
            pygame.mixer.music.load(aud)
            pygame.mixer.music.play()
            started = True
            paused = False
    return started, paused, play_count


def stop(started, paused):
    print('stop function')
    config.started = False
    config.paused = True
    pygame.mixer.music.stop()


def pause(started, paused):
    print('pause function')
    config.paused = True
    pygame.mixer.music.pause()

def unpause(started, paused):
    config.paused = False
    pygame.mixer.music.unpause()

def volumeUp():
    cur_vol = pygame.mixer.get_volume()
    pygame.mixer.set_volume(cur_vol + 0.1)

def volumeDown():
    cur_vol = pygame.mixer.get_volume()
    pygame.mixer.set_volume(cur_vol - 0.1)

def calibrate(r, m):
    with m as source: 
        r.adjust_for_ambient_noise(source)

def speech(commandsqueue):
    r = sr.Recognizer()
    while (1):
        with sr.Microphone() as source:
            print("say something!")
            time.sleep(1)
            audio = r.listen(source)
        try:
            speech = r.recognize_google(audio)
            print("You said: " + speech)

            speech = speech.split()[0]
            # print("Command given: " + speech)

            if speech == "start":
                phrase = "starting text reading"
                # read()
                commandsqueue.put('start')
                # pygame.mixer.music.set_endevent(MUSIC_END)
            elif speech == "stop":
                phrase = "stopping text reading"
                # pause()
                commandsqueue.put('stop')
            elif speech == "pause":
                phrase = "pausing text reading"
                # pause()
                commandsqueue.put('pause')
            elif speech == "play":
                phrase = "resuming text reading"
                commandsqueue.put('unpause')
            elif speech == "louder":
                phrase = "volume up"
            elif speech == "softer":
                phrase = "volume down"
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


def tts(commandsqueue, audioqueue):
    started = False
    paused = False
    play_count = 0
    init()
    while (1):
        ''' 
        try:
            for event in pygame.event.get():
                if event.type == MUSIC_END:
                    print('music end event')
                    #if pygame.mixer.music.get_endevent():
                    #    print('music end event')
                    play_count += 1
                    pygame.mixer.music.set_endevent()
            if pygame.mixer.music.get_endevent():
                print('music end event')
                play_count += 1
                # pygame.mixer.music.set_endevent()
            pass
        except pygame.error as e:
            print(e.args[0])
        '''
        try:
            cmd = commandsqueue.get()
            print(cmd)
            if cmd == 'start':
                print( 'got start' )
                read(audioqueue, started, paused, play_count)
            elif cmd == 'stop':
                stop(started, paused)
            elif cmd == 'pause':
                pause(started, paused)
            elif cmd == 'unpause':
                unpause(started, paused)
           
        except Empty as e:
            pass

        if started and not paused and not pygame.mixer.music.get_busy():
            started = False
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

