import cv2
import numpy as np
import argparse
import imutils
import glob
import os

def detect(c):
    
    """Detect the contours"""
        # initialize the shape name and approximate the contour
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    #Find number of vertices
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
     
    # if the shape has 4 vertices, it is either a square or
    # a rectangle
    if len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

    return shape
thresh_level = 160

card_h = 64
card_w = 89
i=1
images = glob.glob('*.PNG')
for fname in images:
    image = cv2.imread(fname)
    #Grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #Blur the image
    blur = cv2.GaussianBlur(gray,(5,5),0)
    #Threshold image
    retval, thresh = cv2.threshold(blur,thresh_level,255,cv2.THRESH_BINARY)
    mean_c = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 15)
    gaus = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 12)
    #Canny edge detection
    edges = cv2.Canny(blur,50,150,apertureSize = 3)


    _, contours, _ = cv2.findContours(edges, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        M = cv2.moments(contour)
        cX = int((M["m10"] / (M["m00"] + 1e-7))*2)
        cY = int((M["m01"] / (M["m00"] + 1e-7))*2)
        shape = detect(contour)
        area = cv2.contourArea(contour)

        if area > 30000:# and shape == "rectangle":
            cv2.drawContours(image, contour, -1, (0,255,0), 3)
    cv2.imwrite("Detect_card"+str(i)+".PNG", image)
    i+=1


cv2.imshow("image", image)
cv2.imshow("thresh", thresh)
cv2.imshow('canny', edges)

