import speech_recognition as sr
import time
import sys
import threading
import timeit

timeit.template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return _t1 - _t0, retval
"""

r = sr.Recognizer()
m = sr.Microphone()

already_processed = False
counter = 0
total = 0

with m as source: 
	r.adjust_for_ambient_noise(source)

while (1):
    if counter > 20:
        print("avg latency: ", total/counter)
        break
    with sr.Microphone() as source:
        print("say something!")
        time.sleep(1)
        audio = r.listen(source)
    try:

        t = timeit.Timer(lambda: r.recognize_google(audio))
        
        #speech = r.recognize_google(audio)
        print( "exe time: ", t.timeit(number=1)[0])
        speech = t.timeit(number=1)[1]
        print("You said: " + speech)
        # speech = speech.split()[0]
        counter = counter + 1
        total = total + t.timeit(number=1)[0]

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Error; {0}".format(e))



