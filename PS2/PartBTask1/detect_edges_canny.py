import cv2
import numpy as np
import argparse
import imutils
import glob
import os

#Define constants
thresh_level = 160
card_h = 64
card_w = 89
i=1

#Read in images
images = glob.glob('*.PNG')
'''
Iterate over the images and detect the edges
'''
for fname in images:
    image = cv2.imread(fname)
    #Convert to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #Blur the image
    blur = cv2.GaussianBlur(gray,(5,5),0)
    #Threshhold image
    retval, thresh = cv2.threshold(blur,thresh_level,255,cv2.THRESH_BINARY)
    #Use canny edge detection
    edges = cv2.Canny(blur,50,150,apertureSize = 3)
    #Save the images 
    cv2.imwrite("Detect_card"+str(i)+".PNG", edges)
    i+=1


cv2.imshow("image", image)
cv2.imshow("thresh", thresh)
cv2.imshow('canny', edges)

