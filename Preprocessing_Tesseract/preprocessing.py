
import cv2
from matplotlib import pyplot as plt
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Khoa: works on my side with team6.png, printing to console
# page.png works, only prints for noise removal and thick font case
# testimage works, prints for all cases
# Pretty accurate results after noise_removal, bit more acccurate than thick font version

#image_file = "team6.png"
image_file = "page.jpg"
#image_file = "testimage.jpg"
img = cv2.imread(image_file)

def convert(img):
    text = pytesseract.image_to_string(img)
    print(text)

def print_func(header,file):
    print("------------------------------------------")
    print(header)
    convert(file)

def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)

    height, width  = im_data.shape[:2]
    
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()

display(image_file)

print_func("Normal:", image_file )

###### gray and black white image
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


gray_image = grayscale(img)
cv2.imwrite("gray.jpg", gray_image)

thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
cv2.imwrite("bw_image.jpg", im_bw)
display("bw_image.jpg")

print_func("Black and white: ", gray_image)


## Noise Removal
def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)

no_noise = noise_removal(im_bw)
cv2.imwrite("no_noise.jpg", no_noise)

display("no_noise.jpg")

print_func("Noise Removal: ", no_noise)
# thick font

def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)
thick_image = thick_font(no_noise)
cv2.imwrite("thick_image.jpg", thick_image)

display("thick_image.jpg")

print_func("Thick font: ", thick_image)
