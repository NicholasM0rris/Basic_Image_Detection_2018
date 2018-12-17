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
centers=[]
font = cv2.FONT_HERSHEY_SIMPLEX

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

images = glob.glob('*.PNG')
for fname in images:
    image = cv2.imread(fname)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #Blur the image
    blur = cv2.GaussianBlur(gray,(5,5),0)
    retval, thresh = cv2.threshold(blur,thresh_level,255,cv2.THRESH_BINARY)
    mean_c = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 15)
    gaus = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 12)
    edges = cv2.Canny(blur,50,150,apertureSize = 3)

    centers=[]
    _, contours, _ = cv2.findContours(edges, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    #_, contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        
        '''if cv2.contourArea(contour)<100:
            continue
        elif cv2.contourArea(contour)>1000:
            continue
        '''
        M = cv2.moments(contour)
        cX = int(M['m10'] / (M['m00'] + 1e-7))
        cY = int(M['m01'] / (M['m00'] + 1e-7))
        
        
        shape = detect(contour)
        area = cv2.contourArea(contour)
        
        if area > 30000:# and shape == "rectangle":
            cv2.drawContours(image, contour, -1, (0,255,0), 3)
            cv2.circle(image, (cX, cY), 7, (255,0,255), -1)
            centers.append([cX, cY])
    #If there are 2 cards
    if len(centers) == 4:
        #Find distance between cards x and y
        dx = centers[0][0] - centers[2][0]
        dy = centers[0][1] - centers[2][1]
        #Pythag magic
        D = np.sqrt(dx*dx+dy*dy)
        (x1, y1) = centers[0]
        (x2,y2) = centers[2]
        #Draw!
        cv2.putText(image, "Distance: " + str(D), (10, 450), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.line(image, (x1,y1), (x2,y2),(0,0,255), 2,8,0)
        #If there are 3 cards
    elif len(centers) == 6:
        dx1 = centers[0][0] - centers[2][0]
        dy1 = centers[0][1] - centers[2][1]
        D1 = np.sqrt(dx1*dx1+dy1*dy1)
        x_center1 = int(round((centers[0][0] + centers[2][0])/2))
        y_center1 = int(round((centers[0][1] + centers[2][1])/2))
        (x1, y1) = centers[0]
        (x2,y2) = centers[2]
        
        dx2 = centers[0][0] - centers[4][0]
        dy2 = centers[0][1] - centers[4][1]
        D2 = np.sqrt(dx2*dx2+dy2*dy2)
        x_center2 = int(round((centers[0][0] + centers[4][0])/2))
        y_center2 = int(round((centers[0][1] + centers[4][1])/2))
        (x3,y3) = centers[4]

        dx3 = centers[2][0] - centers[4][0]
        dy3 = centers[2][1] - centers[4][1]
        D3 = np.sqrt(dx3*dx3+dy3*dy3)
        x_center3 = int(round((centers[2][0] + centers[4][0])/2))
        y_center3 = int(round((centers[2][1] + centers[4][1])/2))
        
        cv2.line(image, (x1,y1), (x2,y2),(0,0,255), 2,8,0)
        cv2.line(image, (x1,y1), (x3,y3),(0,0,255), 2,8,0)
        cv2.line(image, (x3,y3), (x2,y2),(0,0,255), 2,8,0)
        cv2.putText(image, "Distance: " + str(D1), (x_center1, y_center1+50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "Distance: " + str(D2), (x_center2, y_center2+50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "Distance: " + str(D3), (x_center3, y_center3+50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
    else: #There's one, none of more than 3 cards. Simple should have 3 or less.
        D = 0
        cv2.putText(image, "Distance: " + str(D), (10, 450), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
     #   cv2.line(image, tuple(centers[0].ravel()), tuple(centers[1].ravel()) , (0,255,0), thickness=3, lineType=8)
    


    
        
    cv2.imwrite("Detect_card"+str(i)+".PNG", image)
    
    i+=1

cv2.imshow("image", image)
cv2.imshow("thresh", thresh)
cv2.imshow('canny', edges)

