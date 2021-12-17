# Preprocessing with Pytesseract

*Noise removal*

*Dilated image*

*Grayscale to Black and white*


Bugs (Khoa on my side) :
 
**team6.png** prints for all cases

**page.png** works, only prints for noise removal and thick font case

**testimage.jpg** works, prints for all cases

Pretty accurate results after noise_removal, bit more acccurate than thick font version

Bugs (Josh side):
Preprocessing does not work when using a live taken image

Files:

preprocessing.py --- takes image as input, and does preprocessing three ways as described above, and does OCR text recognition for each preprocessed image. The preprocessed images are saved to the computer.

preprocessing_WithWebCam.py --- same as above, but live pictures of sample are taken, instead of using images already on the computer.

Bugs:
Sometimes images are shown all black when taken with webcam after preprocessing; thus, no text is recognized and outputted.

Future Improvements:
Fix webcam and preprocessing integration. Also, integrate preprocessing OCR with preprocessing with other modules.

Sources:
https://www.youtube.com/watch?v=ADV-AjAXHdc


