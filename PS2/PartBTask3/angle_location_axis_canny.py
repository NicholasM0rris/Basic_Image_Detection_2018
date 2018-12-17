import cv2
import numpy as np
import argparse
import imutils
import glob
import os
import math

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
    '''
    edges_f = np.float32(edges)
    corners = cv2.goodFeaturesToTrack(edges_f, 100, 0.01, 10)
    corners = np.int0(corners)
    for corner in corners:
        
        xp, yp = corner.ravel()
        cv2.circle(image, (xp, yp), 3, 255, -1)
    '''
    centers=[]
    angles = []

   
    _, contours, _ = cv2.findContours(edges, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    #_, contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        
        '''if cv2.contourArea(contour)<100:
            continue
        elif cv2.contourArea(contour)>1000:
            continue
        '''
        #Get center contour (card)
        M = cv2.moments(contour)
        cX = int(M['m10'] / (M['m00'] + 1e-7))
        cY = int(M['m01'] / (M['m00'] + 1e-7))
        
        
        shape = detect(contour)
        area = cv2.contourArea(contour)
        
        if area > 30000:# and shape == "rectangle":
            cv2.drawContours(image, contour, -1, (0,255,0), 3)
            #Draw a circle at the center of card
            cv2.circle(image, (cX, cY), 7, (255,0,255), -1)
            #Get bounding box coords
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            width, height = rect[1]
            #Extract angle
            if width > height:
                w = height
                height = width
                width = w
                angle = -1*rect[2]+ 90
            else:
                angle = -1*rect[2]
            centers.append([cX, cY])
            angles.append(angle)
            

    if len(centers) == 4:
        #Print no cards
        cv2.putText(image, "No. Cards: 2", (500, 100), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        #Get the centers and angles
        (x1, y1) = centers[0]
        (x2,y2) = centers[2]
        angle1 = angles[0]
        angle2 = angles[2]
        #Draw lines for the axis. 
        (x1_a, y1_a) = (int(round(x1+150*math.sin(math.radians(angle1+90)))), int(round(y1+150*math.cos(math.radians(angle1+90)))))
        cv2.line(image, (x1,y1),(x1_a, y1_a), (0,0,255), 5)
        cv2.line(image, (x1,y1), (x1+150, y1), (0,0,255), 5)
        (x2_a, y2_a) = (int(round(x2+150*math.sin(math.radians(angle2+90)))), int(round(y2+150*math.cos(math.radians(angle2+90)))))
        cv2.line(image, (x2,y2),(x2_a, y2_a), (0,0,255), 5)
        cv2.line(image, (x2,y2), (x2+150, y2), (0,0,255), 5)
    
        cv2.line(image, (x1,y1), (x1+100, y1), (0,0,255), 3)
        cv2.line(image, (x2,y2), (x2+100, y2), (0,0,255),3 )
        #Angle and location print
        cv2.putText(image, "Angle: " + str(angle1), (x1-200, y1+200), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "Angle: " + str(angle2), (x2-200, y2+200), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "Location: " + str(x1) + ", " + str(y1), (x1-200, y1+50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "Location: " + str(x2) + ", " + str(y2), (x2-200, y2+50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
      
        #Same as above
    elif len(centers) == 6:
        cv2.putText(image, "No. Cards: 3", (500, 100), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

        
        (x1, y1) = centers[0]
        (x2,y2) = centers[2]

        (x3,y3) = centers[4]
        angle1 = angles[0]
        angle2 = angles[2]
        angle3 = angles[4]
        (x1_a, y1_a) = (int(round(x1+150*math.sin(math.radians(angle1+90)))), int(round(y1+150*math.cos(math.radians(angle1+90)))))
        cv2.line(image, (x1,y1),(x1_a, y1_a), (0,0,255), 5)
        cv2.line(image, (x1,y1), (x1+150, y1), (0,0,255), 5)
        (x2_a, y2_a) = (int(round(x2+150*math.sin(math.radians(angle2+90)))), int(round(y2+150*math.cos(math.radians(angle2+90)))))
        cv2.line(image, (x2,y2),(x2_a, y2_a), (0,0,255), 5)
        cv2.line(image, (x2,y2), (x2+150, y2), (0,0,255), 5)
        (x3_a, y3_a) = (int(round(x3+150*math.sin(math.radians(angle3+90)))), int(round(y3+150*math.cos(math.radians(angle3+90)))))
        cv2.line(image, (x3,y3),(x3_a, y3_a), (0,0,255), 5)
        cv2.line(image, (x3,y3), (x3+150, y3), (0,0,255), 5)

        
        cv2.line(image, (x1,y1), (x1+100, y1), (0,0,255), 3)
        cv2.line(image, (x2,y2), (x2+100, y2), (0,0,255),3 )
        cv2.line(image, (x3,y3), (x3+100, y3), (0,0,255), 3)
        cv2.putText(image, "Angle: " + str(angle1), (x1-200, y1+200), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "Angle: " + str(angle2), (x2-200, y2+200), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "Angle: " + str(angle3), (x3-200, y3+200), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "Location: " + str(x1) + ", " + str(y1), (x1-200, y1+50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "Location: " + str(x2) + ", " + str(y2), (x2-200, y2+50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "Location: " + str(x3) + ", " + str(y3), (x3-200, y3+50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
    else:#Same as above
        if len(centers) > 1:
            cv2.putText(image, "No. Cards: 1", (500, 100), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

            
        D = 0
        (x1, y1) = centers[0]
        angle1 = angles[0]
        (x1_a, y1_a) = (int(round(x1+150*math.sin(math.radians(angle1+90)))), int(round(y1+150*math.cos(math.radians(angle1+90)))))
        cv2.line(image, (x1,y1),(x1_a, y1_a), (0,0,255), 5)
        cv2.line(image, (x1,y1), (x1+150, y1), (0,0,255), 5)
        cv2.putText(image, "Angle: " + str(angle1), (10,100), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "Location: " + str(x1) + ", " + str(y1), (x1-200, y1+50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
     #   cv2.line(image, tuple(centers[0].ravel()), tuple(centers[1].ravel()) , (0,255,0), thickness=3, lineType=8)
    
        

    
        
    cv2.imwrite("Detect_card"+str(i)+".PNG", image)
    
    i+=1

cv2.imshow("image", image)
cv2.imshow("thresh", thresh)
cv2.imshow('canny', edges)

