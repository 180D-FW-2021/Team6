# TechVidvan hand Gesture Recognizer

# import necessary packages

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
'''
mpHands = None
hands = None
mpDraw = None
model = None
classNames = None
cap = None
counter = 0
pose = None
'''

# path arg is path of Team6 folder
def init(commandsqueue, path, conn1):
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
            cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, \
                    cv2.LINE_AA)
        
        # Show the final output
        # Uncomment to show pose recognition window
        # cv2.imshow("Output", frame)
        conn1.send(frame)
        
        if counter > 5: 
            if className == 'stop': 
                print("pose: stop")
                commandsqueue.put('stop')

            elif className == 'thumbs up':
                print("pose: start")
                commandsqueue.put('start')
            counter = 0
        if pose == className: 
            counter = counter + 1 
        
        pose = className 

        if cv2.waitKey(1) == ord('q'):
            break

    # release the webcam and destroy all active windows
    cap.release()
    
    cv2.destroyAllWindows()

# import os
# path = os.getcwd()
# init(path)
# loop()
# cleanup()

