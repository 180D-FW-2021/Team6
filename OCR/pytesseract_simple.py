import pytesseract
import cv2 # faster than PIL

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def noise_removal(image):
    return cv2.medianBlur(image,5)

def threshold(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
def convert(img):
    text = pytesseract.image_to_string(img)
    return text

def process():
    img = cv2.imread('handwriting.jpg')   
    img = grayscale(img)
    img = threshold(img)
    img = noise_removal(img)
    #cv2.imwrite("processed_image.png",img)
    #cv2.imshow('window',test)
    print(convert(img))

process()


