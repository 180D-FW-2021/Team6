# based on https://stackoverflow.com/a/57387909, to get non-blocking console input 
# test that motors are working given console stdin

import sys
import threading
import flip
import time


key_in = ''
servo = None
motorF = None
led = None


class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return


def my_callback(inp):
    #evaluate the keyboard input
    print('You Entered:', inp)
    global key_in
    key_in = inp

#start the Keyboard thread
kthread = KeyboardThread(my_callback)
flipforwardthread = None
flipbackwardsthread = None

flip.init()

while True:
    if (key_in == 'f'):
        flipfowardthread = threading.Thread(target=flip.pageturn_forward(), name='foward', args=(1,))
        flipfowardthread.start()
        print('forward start')
        key_in = ''
    elif (key_in == 'b'):
        flipbackwardsthread = threading.Thread(target=flip.pageturn_backwards(), name='backwards', args=(1,))
        flipbackwardsthread.start()
        key_in = ''
   
'''
if __name__ == '__main__':
    main()
'''
