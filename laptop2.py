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
import config
import speech_tts.tts1 as speechtts 
import hand_gesture_recognition_code.TechVidvan_hand_gesture_detection as pose
# import Communications.gesture_control_subscriber as comms


process_text_mutex = threading.Lock()

def test_text_recognition():
    sampletextfile = []
    # sampletextfile.append(open('speech_tts/testing/sampletext'))
    # sampletextfile.append(open('speech_tts/testing/sampletext1000'))
    # sampletextfile.append(open('speech_tts/testing/sampletext'))
    sampletextfile.append(open('speech_tts/testing/sampletext_short1'))
    sampletextfile.append(open('speech_tts/testing/sampletext_short2'))
    sampletextfile.append(open('speech_tts/testing/sampletext_short3'))
    while (1):
        if len(sampletextfile) > 0:
            process_text_mutex.acquire()
            config.sampleText.append(sampletextfile[0].read())
            sampletextfile.pop(0)
            process_text_mutex.release()
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
def on_message(client, userdata, message):
    text_file = open("sample.txt","wt")
    n = text_file.write('Received message: "' + str(message.payload) + '"on topic "' + \
            message.topic + '" with QoS ' + str(message.qos))
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

def main():
    # global config.sampleText
    
    path = os.getcwd()
    speechtts.init()
    pose.init(path)

    t1 = threading.Thread(target=test_text_recognition, args=()) 
    t2 = threading.Thread(target=speechtts.speech, args=()) 
    t3 = threading.Thread(target=pose.loop, args=(speechtts.read, speechtts.pause)) 
    t4 = threading.Thread(target=speechtts.tts, args=()) 

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    # pose.cleanup()

if __name__ == '__main__':
    main()

