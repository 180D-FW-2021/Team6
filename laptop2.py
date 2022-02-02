import os
import threading

import paho.mqtt.client as mqtt
import pyttsx3
import speech_recognition as sr
import time
import sys
import pygame
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# TechVidvan hand Gesture Recognizer
import README_UI as UI
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

import OCR.OCR as pytest
import pytesseract
process_text_mutex = threading.Lock()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

client = None


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


# def image_test():
#     img = cv2.imread("image1.jpg", cv2.IMREAD_COLOR)
#     process_text_mutex.acquire()
#     config.ImagePass = "image1.jpg"
#     # save the processed text in 'text' to send with mqtt
#     text = pytesseract.image_to_string(img)
#     config.gotImage = 1
#     config.sampleText = text
#     process_text_mutex.release()
#     speechtts.process_text()
#     config.gotImage = 0

# def image_test():
#     img = cv2.imread("image1.jpg", cv2.IMREAD_COLOR)
#     config.ImagePass = "image1.jpg"
#     process_text_mutex.acquire()
#     gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     kernel = np.ones((1, 1), np.uint8)
#     nn = cv2.dilate(gray_image, kernel, iterations=1)
#     kernel = np.ones((1, 1), np.uint8)
#     nn = cv2.erode(gray_image, kernel, iterations=1)
#     nn = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)
#     nn = cv2.medianBlur(gray_image, 3)
#     cv2.imwrite("image1_processed.jpg", nn)
#
#     # save the processed text in 'text' to send with mqtt
#     text = pytesseract.image_to_string(nn)
#     config.gotImage = 1
#     config.sampleText = text
#     process_text_mutex.release()
#     speechtts.process_text()
#     config.gotImage = 0
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


# def on_message(client, userdata, message):
#    print( "message received" )
#    print(str(message.payload))
#    process_text_mutex.acquire()
#    config.sampleText.append(str(message.payload))
#    process_text_mutex.release()
#    speechtts.process_text()

# with image
# def on_message(client, userdata, message):
#     img = cv2.imread("image1.jpg", cv2.IMREAD_COLOR)
#     process_text_mutex.acquire()
#     config.ImagePass = "image1.jpg"
#     # save the processed text in 'text' to send with mqtt
#     text = pytesseract.image_to_string(img)
#     config.gotImage = 1
#     config.sampleText.append(text)
#     process_text_mutex.release()
#     speechtts.process_text()


def on_message(client, userdata, message):
    f = open('receive.jpg', 'wb')
    f.write(message.payload)
    f.close()
    print('image received')
    img = cv2.imread("receive.jpg", cv2.IMREAD_COLOR)
    text = pytesseract.image_to_string(img)
    print(text)
    process_text_mutex.acquire()
    config.ImagePass = "receive.jpg"
    config.sampleText = text
    # config.sampleText.append(text)

    process_text_mutex.release()
    speechtts.process_text()


def text_recognition():
    # 1. create a client instance.
    client = mqtt.Client()
    # add additional clientoptions (security, certifications, etc.)
    # many default options should be good to start off.
    # add callbacks to client.

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # 2. connect to a broker using one of the connect*() functions.5

    client.connect_async('test.mosquitto.org')
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

    # pose.setup()

    path = os.getcwd()
    speechtts.init()
    pose.init(path)

    t1 = threading.Thread(target=UI.setup, args=())
    t2 = threading.Thread(target=speechtts.speech, args=())
    t3 = threading.Thread(target=pose.loop, args=(
        speechtts.read, speechtts.pause))
    t4 = threading.Thread(target=speechtts.tts, args=())
    t5 = threading.Thread(target=text_recognition, args=())

    t5.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()

    pose.cleanup()
    # sys.exit(app.exec_())
    # sys.exit()


if __name__ == '__main__':
    main()
