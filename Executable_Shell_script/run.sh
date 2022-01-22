#!/bin/bash


#input 0 to install 
#input 1 to just run code 
#input 2 to install then run code 

#install 
if [ "$1" -eq "0" ] || [ "$1" -eq "2" ]
then 
    pip install pytesseract 
    pip install numpy
    pip install opencv-python

fi

#run 
if [ "$1" -eq "1" ] || [ "$1" -eq "2" ]
then 
    echo "Run code"
fi
