import easyocr as ocr  
import streamlit as st  
from PIL import Image 
import numpy as np 

#title
st.title("ReadMe - Team 6")

#subtitle
st.markdown("## EasyOCR Test Web App")

st.markdown("")

#image uploader
image = st.file_uploader(label = "Upload your image here (png,jp, or jpeg)",type=['png','jpg','jpeg'])


@st.cache
def load_model(): 
    reader = ocr.Reader(['en'],model_storage_directory='.')
    return reader 

reader = load_model() #load model

if image is not None:

    input_image = Image.open(image) #read image
    st.image(input_image) #display image

    with st.spinner("Please wait"):
        

        result = reader.readtext(np.array(input_image))

        result_text = [] #empty list for results


        for text in result:
            result_text.append(text[1])

        st.write(result_text)
    #st.balloons()
else:
    st.write("Upload an Image")







