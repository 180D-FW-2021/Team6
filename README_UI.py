
from PyQt5 import QtGui
import pytesseract
import sys
import cv2
import re
import numpy as np
import config
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from UI.Instructions_Pop_up import Ui_MainWindow
#from UI.Instructions_Pop_up import *

from PIL import Image 
import PIL
import os 

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        # cap = cv2.VideoCapture(0)
        while self._run_flag:
            # print('webcam') # for some reason, this makes it less laggy?
            if config.frame is not None:
                cv_img = config.frame
                self.change_pixmap_signal.emit(cv_img)
        #    ret, cv_img = cap.read()
        #    if ret:
        #        self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        # cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    # Main Screen areas
    def __init__(self):
        super().__init__()
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.setWindowTitle("READEME")
        self.resize(1920, 1080)

        timer = QTimer(self)
        timer.timeout.connect(self.updateScreen)
        timer.start(10)

        # Image area ---------------------------------------------------
        self.labelImage = QLabel(self)
        self.labelImage.setGeometry(QtCore.QRect(30, 50, 711, 470))
        self.labelImage.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.labelImage.setText("")
        self.labelImage.setObjectName("labelImage")
        self.labelImage.setScaledContents(True)
        # Image area ---------------------------------------------------

        # Text area ------------------------------------------------------
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(1000, 50, 711, 470))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.textEdit.setFont(font)
        self.textEdit.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setObjectName("textEdit")
        # Text area ------------------------------------------------------

        # Webcam -------------------------------------------------------
        self.Webcam = QLabel(self)
        # self.Webcam.resize(640, 640)
        self.Webcam.setGeometry(QtCore.QRect(1040, 550, 711, 470))
        self.textLabel = QLabel('Webcam')
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        # Webcam -------------------------------------------------------

        # Buttons ------------------------------------------------------------
        self.Loadimage = QPushButton("Load Image", self)
        self.Loadimage.setObjectName("Load Image")
        self.Loadimage.setGeometry(QtCore.QRect(225, 545, 250, 41))
        self.Loadimage.resize(250, 75)
        self.Loadimage.setFont(QFont('Times', 15))
        self.Loadimage.clicked.connect(self.getImage)
        self.Loadimage.setStyleSheet("""
        QPushButton {
            background:rgb(255, 255, 255); 
            border: 2px solid black;
            border-radius: 15px;
        }
        QPushButton:hover {
             background-color: lightgreen;
        }
        """)

        self.Run = QPushButton("Run", self)
        self.Run.setObjectName("Run")
        self.Run.setGeometry(QtCore.QRect(225, 625, 250, 41))
        self.Run.resize(250, 75)
        self.Run.setFont(QFont('Times', 15))
        self.Run.clicked.connect(self.extractText)
        self.Run.setStyleSheet("""
        QPushButton {
            background:rgb(255, 255, 255); 
            border: 2px solid black;
            border-radius: 15px;
        }
        QPushButton:hover {
             background-color: lightgreen;
        }
        """)

        self.Clear = QPushButton("Clear", self)
        self.Clear.setObjectName("Clear")
        self.Clear.setGeometry(QtCore.QRect(225, 705, 250, 41))
        self.Clear.resize(250, 75)
        self.Clear.setFont(QFont('Times', 15))
        self.Clear.clicked.connect(self.clearText)
        self.Clear.setStyleSheet("""
        QPushButton {
            background:rgb(255, 255, 255); 
            border: 2px solid black;
            border-radius: 15px;
        }
        QPushButton:hover {
             background-color: lightgreen;
        }
        """)

        self.Save = QPushButton("Save text", self)
        self.Save.setObjectName("Save text")
        self.Save.setGeometry(QtCore.QRect(225, 785, 250, 41))
        self.Save.resize(250, 75)
        self.Save.setFont(QFont('Times', 15))
        self.Save.clicked.connect(self.saveText)
        self.Save.setStyleSheet("""
        QPushButton {
            background:rgb(255, 255, 255); 
            border: 2px solid black;
            border-radius: 15px;
        }
        QPushButton:hover {
             background-color: lightgreen;
        }
        """)

        self.SaveImage = QPushButton("Save Image", self)
        self.SaveImage.setObjectName("Save Image")
        self.SaveImage.setGeometry(QtCore.QRect(225, 865, 250, 41))
        self.SaveImage.resize(250, 75)
        self.SaveImage.setFont(QFont('Times', 15))
        self.SaveImage.clicked.connect(self.saveImage)
        self.SaveImage.setStyleSheet("""
        QPushButton {
            background:rgb(255, 255, 255); 
            border: 2px solid black;
            border-radius: 15px;
        }
        QPushButton:hover {
             background-color: lightgreen;
        }
        """)

        self.Instructions = QPushButton("Instructions", self)
        self.Instructions.setObjectName("Instructions")
        self.Instructions.setGeometry(QtCore.QRect(225, 945, 250, 41))
        self.Instructions.resize(250, 75)
        self.Instructions.setFont(QFont('Times', 15))
        self.Instructions.clicked.connect(self.openWindow)
        self.Instructions.setStyleSheet("""
        QPushButton {
            background:rgb(255, 255, 255); 
            border: 2px solid black;
            border-radius: 15px;
        }
        QPushButton:hover {
             background-color: lightgreen;
        }
        """)
        # self.Exit = QPushButton("Exit", self)
        # self.Exit.setObjectName("Exit")
        # self.Exit.setGeometry(QtCore.QRect(30, 860, 171, 41))
        # self.Exit.resize(200, 50)
        # self.Exit.setFont(QFont('Times', 15))
        # self.Exit.clicked.connect(self.close)

        # Buttons ------------------------------------------------------------
    

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the Webcam with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.Webcam.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(
            640, 480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def close(self):
        cv2.destroyAllWindows()
        exit()

    def getImage(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            options=options)
        # self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Open a image", "","All Files (*);;Image Files (*.jpg);;Image Files (*.png)", options=options)
        if self.fileName:
            print(self.fileName)
            self.img = cv2.imread(self.fileName)
            #1 GRAY
            self.gray_image = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("gray.jpg", self.gray_image)
            #2 BW
            #thresh, self.bw = cv2.threshold(self.gray_image, 210, 230, cv2.THRESH_BINARY)
            thresh, self.bw = cv2.threshold(self.gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            cv2.imwrite("bw_image.jpg", self.bw)

            ##########
            #3 GRAY-> BLACK and WHITE -> DILATION
            self.bt = cv2.bitwise_not(self.bw)
            kernel = np.ones((1,1),np.uint8) #increase 2,2 to 3,3 for stronger dilation, 5,5 is too
            self.bt = cv2.dilate(self.bt, kernel, iterations=1)
            self.bt = cv2.bitwise_not(self.bt)

            #4 GRAY-> BLACK and WHITE -> DILATION -> NOISE REMOVAL
            '''
            kernel = np.ones((1, 1), np.uint8)
            self.nn = cv2.dilate(self.bt, kernel, iterations=1)
            self.nn = cv2.erode(self.nn, kernel, iterations=1)
            self.nn = cv2.morphologyEx(self.nn, cv2.MORPH_CLOSE, kernel)
            self.nn = cv2.medianBlur(self.nn, 3)'''

            #5 Noise removal and erosion
            # GRAY > BLACK WHITE#2 > NOISE REMOVAL
            '''kernel = np.ones((1, 1), np.uint8)
            self.nn = cv2.dilate(self.bw, kernel, iterations=1)
            self.nn = cv2.erode(self.nn, kernel, iterations=1)
            self.nn = cv2.morphologyEx(self.nn, cv2.MORPH_CLOSE, kernel)
            self.nn = cv2.medianBlur(self.nn, 3)'''
            # Dilation

            # GRAY > BLACK WHITE > NOISE REMOVAL > DILATION
            '''self.bt = cv2.bitwise_not(self.nn)
            kernel = np.ones((2,2),np.uint8) #increase 2,2 to 3,3 for stronger dilation, 5,5 is too
            self.bt = cv2.dilate(self.bt, kernel, iterations=1)
            self.bt = cv2.bitwise_not(self.bt)'''
            # GRAY > BLACK WHITE > DILATION
            '''self.bt = cv2.bitwise_not(self.bw)
            kernel = np.ones((2,2),np.uint8) #increase 2,2 to 3,3 for stronger dilation, 5,5 is too
            self.bt = cv2.dilate(self.bt, kernel, iterations=1)
            self.bt = cv2.bitwise_not(self.bt)'''
            #cv2.imwrite("no_noise.jpg", self.nn)
            cv2.imwrite("dilated.jpg", self.bt)
            pattern = ".(jpg|png|jpeg|bmp|jpe|tiff)$"
            self.fileName2 = "dilated.jpg"
            #self.fileName2 = "no_noise.jpg"
            if re.search(pattern, self.fileName2):
                # self.setImage(self.fileName)
                self.setImage(self.fileName)

    def setImage(self, fileName):
        self.labelImage.setPixmap(QPixmap(fileName))
        self.Run.setEnabled(True)

    def extractText(self):
        config = ('-l eng --oem 1 --psm 3')
        img = cv2.imread(self.fileName2, cv2.IMREAD_COLOR)
        # Run tesseract OCR on image
        text = pytesseract.image_to_string(img, config=config)
        # Print recognized text
        self.textEdit.append(text)
        print(text)

    def clearText(self):
        self.textEdit.clear()

    def saveText(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        # fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save text","All Files (*);;Text Files (*.txt)", options=options)
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(options=options)
        if fileName:
            print(fileName)
            file = open(fileName, 'w')
            text = self.textEdit.toPlainText()
            file.write(text)
            file.close()

    def saveImage(self):
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            split_tup = os.path.splitext(fileName)
            pixmap = self.labelImage.pixmap()
            if pixmap is not None and fileName:
                if not split_tup[1]:
                    jpg ='.jpg'
                    pixmap.save(fileName+jpg)    
                else:
                    pixmap.save(fileName)
        
            


    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def setText(self, text):
        #strC = self.listToString(text)
        strC = text[-1]
        self.textEdit.append(strC)

    def updateScreen(self):
        if config.start == 1:
            print(config.sampleText)
            self.setText(config.sampleText)
            self.setImage(config.ImagePass)
            config.start = 0

    def listToString(self, s):

        # initialize an empty string
        str1 = " "

        # return string
        return (str1.join(s))


def setup():
    app = QApplication(sys.argv)
    a = App()
    c = a.palette()
    c.setColor(a.backgroundRole(), Qt.gray)
    a.setPalette(c)
    a.show()
    sys.exit(app.exec_())

    # app.exec_()
    # sys.exit()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    c = a.palette()
    c.setColor(a.backgroundRole(), Qt.gray)
    a.setPalette(c)
    a.show()
    #a.setText("THis is a test")
    # a.setImage()
    sys.exit(app.exec_())
