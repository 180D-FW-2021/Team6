from multiprocessing import Process
import os

def speech_recognition(title):
    print(title)

def gesture_recognition(title):
    print(title)

def pose_recognition(title):
    print(title)

if __name__ == '__main__':
    info('main line')
    
	
    p1 = Process(target=speech_recognition, args=(title))
    p1.start()
    # p1.join()

    p2 = Process(target=gesture_recognition, args=(title))
    p2.start()
    # p2.join()

    p3 = Process(target=pose_recognition, args=(title))
    p3.start()
    # p3.join()

    p1.join()
    p2.join()
    p3.join()
