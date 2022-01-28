import os
import threading

import paho.mqtt.client as mqtt
import pyttsx3
import speech_recognition as sr
import time
import sys
import pygame

# TechVidvan hand Gesture Recognizer

# import necessary packages

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

# import functions
from speech_tts import tts1 as speechtts 
from hand_gesture_recognition_code import TechVidvan_hand_gesture_detection as pose
# from Communications import gesture_control_subscriber as comms

# global variables

sampleText = ""
engine = None
r = None
m = None
already_processed = False
outfile = None

process_text_mutex = threading.Lock()

def test_text_recognition():
    global sampleText
    sampletextfile = open('speech_tts/testing/sampletext1000')
    sampleText = sampletextfile.read()
    speechtts.process_text()

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
        print("Connection returned result: "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("ece180d/text", qos=1)

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
        if rc != 0:
                print('Unexpected Disconnect')
        else:
                print('Expected Disconnect')

# The default message callback.
# (you can create separate callbacks per subscribed topic)
'''
    text_file = open("sample.txt","wt")
    n = text_file.write()
    sampleText = open(sys.argv[1], "r")
    #sampleText = sampletextfile.read()
    speech_and_text(sampleText)
    print('Received message: "' + str(message.payload) + '"on topic "' + message.topic + '" with QoS ' + str(message.qos))
'''
def on_message(client, userdata, message):
    text_file = open("sample.txt","wt")
    n = text_file.write('Received message: "' + str(message.payload) + '"on topic "' + message.topic + '" with QoS ' + str(message.qos))
    text_file.close()
    #sampletextfile = open(sys.argv[1], "r")
    sampletextfile = open("sample.txt", "r")
    sampleText = sampletextfile.read()
    speechtts.process_text()
        
def text_recognition():
    # 1. create a client instance.
    client = mqtt.Client()
    # add additional client options (security, certifications, etc.)
    # many default options should be good to start off.
    # add callbacks to client.

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # 2. connect to a broker using one of the connect*() functions.5

    client.connect_async('mqtt.eclipseprojects.io')
    # client.connect("mqtt.eclipse.org")

    # 3. call one of the loop*() functions to maintain network traffic flow with the broker.
    client.loop_start()
    # client.loop_forever()

    while True:
        pass

   
    # use subscribe() to subscribe to a topic and receive messages.

    # use publish() to publish messages to the broker.

    # use disconnect() to disconnect from the broker.
    client.loop_stop()
    client.disconnect()


def pose_recognition(path):
        global engine, r, m, already_processed
        
        # initialize mediapipe
        mpHands = mp.solutions.hands
        hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        mpDraw = mp.solutions.drawing_utils

        # Load the gesture recognizer model
        model = load_model(path + '\hand_gesture_recognition_code\mp_hand_gesture')

        # Load class names
        f = open(path + '\hand_gesture_recognition_code\gesture.names', 'r')
        classNames = f.read().split('\n')
        f.close()
        print(classNames)


        # Initialize the webcam
        cap = cv2.VideoCapture(0)

        counter = 0 
        pose = "" 

        while True:
                # Read each frame from the webcam
                _, frame = cap.read()
                        
                x, y, c = frame.shape
                        
                # Flip the frame vertically
                frame = cv2.flip(frame, 1)
                framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                # Get hand landmark prediction
                result = hands.process(framergb)
                        
                # print(result)
                
                className = ''
                        
                # post process the result
                if result.multi_hand_landmarks:
                        landmarks = []
                        for handslms in result.multi_hand_landmarks:
                                for lm in handslms.landmark:
                                        # print(id, lm)
                                        lmx = int(lm.x * x)
                                        lmy = int(lm.y * y)

                                        landmarks.append([lmx, lmy])

                                # Drawing landmarks on frames
                                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
                                
                                # Predict gesture
                                prediction = model.predict([landmarks])
                                # print(prediction)
                                classID = np.argmax(prediction)
                                className = classNames[classID]
                
                # show the prediction on the frame
                if className == 'stop' or className == 'thumbs up': 
                        cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                
                # Show the final output
                cv2.imshow("Output", frame)
                
                if counter > 5: 
                        if className == 'stop': 
                                print("stop")
                                speechtts.pause()
                        elif className == 'thumbs up':
                                print("start")
                                speechtts.read()
                        counter = 0
                if pose == className: 
                        counter = counter + 1 
                
                pose = className 
                                

                if cv2.waitKey(1) == ord('q'):
                        break

        # release the webcam and destroy all active windows
        cap.release()

        cv2.destroyAllWindows()


def pose_recognition_mock():
    while(1):
        pass

def main():
    path = os.getcwd()
    speechtts.init()
    # pose.init(path)

    print('speech init done')

    t1 = threading.Thread(target=test_text_recognition, args=()) 
    t2 = threading.Thread(target=speechtts.speech_and_text, args=()) 
    t3 = threading.Thread(target=pose_recognition, args=(path,)) 

    print('before thread start')

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

if __name__ == '__main__':
    main()
