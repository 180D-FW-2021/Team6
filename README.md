# Team6
ReadMe
Project Overview:
Read your textbooks with our page-turning robot and accompanying app! It will turn the pages of your textbook for you and automatically scan the page to produce the audio file for you to listen to.

Folders: 

Communications: Mqtt connection files 

OCR: Pytesseract OCR testing files 

Preprocessing_Tesseract: adding preprocessing to pytesseract

Tesseract: Pytesseract test code with webcam 

Hand-gesture-recognition-code: Gesture library

IMUGestureControl: code for sampling gesture data, Tensorflow Lite model training, and classifying for imu gesture control

Page_flipper: code for page flipper 

Speech_tts: Text to speech code 

Files:

laptop2.py - main script for laptop

config.py - holds global vars

README_UI.py - class library for GUI

How to run project: 
- Start the "laptop.py" file in the Multiprocessing folder on user's laptop. 
- After mounting textbook under camera/webcam, start the PytesseractTest.py file in OCR folder to take the picture of the image.  To take a picture, press 's' and press 'q' to exit. 
- Upload the "IMU_Classifier.ino" file in the IMUGestureControl folder to your Arduino 33 BLE Sense to enable IMU gesture control. 
- Upload the "esp_flip.ino" file in the page_flipper folder to your ESP32 to enable page flipping.
- Once text has is processed, say "start" into user's laptop's microphone to begin the text reading.  
- Use "start", "stop" voice commands or thumbs up and hand up to start and stop the text reading.  
- Once the reading is done, shake the Arduino 33 BLE Sense controller right or left to enable robotic page flipping to begin reading the next page.
