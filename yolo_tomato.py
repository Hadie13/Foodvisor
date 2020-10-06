# -*- coding: utf-8 -*-
"""
Created on thu Sep  29 14:09:09 2020

@author: Hadie
"""
####### Loading the YOLO model ########

# Import libraries
from darkflow.net.build import TFNet
import cv2
import tensorflow as tf

# Let's config TF
config = tf.ConfigProto(log_device_placement = False)
config.gpu_options.allow_growth = False 

with tf.Session(config=config) as sess:
    options = {
            'model': './cfg/yolo.cfg',
            'load': './yolov2.weights',
            'threshold': 0.6,
            #'gpu': 1.0 
               }
    tfnet = TFNet(options) 
    
# Load and convert images
img = cv2.imread('./sample_img/sample_horses.jpg') # Images for the general yolo model, not for our custom tomato model yet
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
results = tfnet.return_predict(img)
print(results)

# Dislay the results using OpenCV
img = cv2.imread('./sample_img/sample_horses.jpg') # Images for the general yolo model, not for our custom tomato model yet
for (i, result) in enumerate(results):
    x = result['topleft']['x']
    w = result['bottomright']['x']-result['topleft']['x']
    y = result['topleft']['y']
    h = result['bottomright']['y']-result['topleft']['y']
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    label_position = (x + int(w/2)), abs(y - 10)
    cv2.putText(img, result['label'], label_position , cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2)

cv2.imshow("Objet Detection YOLO", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Let's just encapsulate that OpenCV display method into a function
def displayResults(results, img):
    for (i, result) in enumerate(results):
        x = result['topleft']['x']
        w = result['bottomright']['x']-result['topleft']['x']
        y = result['topleft']['y']
        h = result['bottomright']['y']-result['topleft']['y']
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        label_position = (x + int(w/2)), abs(y - 10)
        cv2.putText(img, result['label'], label_position , cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2)
    return img

######## Running YOLO on a video ##########
# Import OpenCV
import cv2
cap = cv2.VideoCapture('Hadiza_test.mp4')
frame_number = 0
while True:
    ret, frame = cap.read()
    frame_number += 1
    if ret:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = tfnet.return_predict(img)
        
        for (i, result) in enumerate(results):
            x = result['topleft']['x']
            w = result['bottomright']['x']-result['topleft']['x']
            y = result['topleft']['y']
            h = result['bottomright']['y']-result['topleft']['y']
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            label_position = (x + int(w/2)), abs(y - 10)
            cv2.putText(frame, result['label'], label_position , cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2)

        cv2.imshow("Objet Detection YOLO", frame)
        if frame_number == 240:
            break
        if cv2.waitKey(1) == 13:
            break

cap.release()
cv2.destroyAllWindows()

###########################################################################
############################# TOMATO MODEL ################################
###########################################################################

#################### Loading my Custom Dataset Model ######################

from darkflow.net.build import TFNet
import cv2
import tensorflow as tf

config = tf.ConfigProto(log_device_placement = False)
config.gpu_options.allow_growth = False 

with tf.Session(config=config) as sess:
    options = {
            'model': './cfg/yolo_1_class.cfg',
            'load': 400, 
            'threshold': 0.45, 
            #'gpu': 1.0 
               }
    tfnet = TFNet(options)   
    
################## Let's test our new Tomato Detector! ####################

# We're going to cycle through 10 images 
for i in range(1,12):
    file_name = './assignment_imgs/img_' + str(i) + '.jpg'
    img = cv2.imread(file_name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = tfnet.return_predict(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    for (i, result) in enumerate(results):
        x = result['topleft']['x']
        w = result['bottomright']['x']-result['topleft']['x']
        y = result['topleft']['y']
        h = result['bottomright']['y']-result['topleft']['y']
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        label_position = (x + int(w/2)), abs(y - 10)
        cv2.putText(img, result['label'], label_position , cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,0), 2)

    cv2.imshow("Objet Detection YOLO", img)
    cv2.waitKey(0)
cv2.destroyAllWindows()

# Let's test this on a video
import cv2

# Using OpenCV to initialize the webcam
cap = cv2.VideoCapture('assiettes_tomates.mp4')
frame_number = 0
while True:
    ret, frame = cap.read()
    frame_number += 1
    if ret:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = tfnet.return_predict(img)
        
        for (i, result) in enumerate(results):
            x = result['topleft']['x']
            w = result['bottomright']['x']-result['topleft']['x']
            y = result['topleft']['y']
            h = result['bottomright']['y']-result['topleft']['y']
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            label_position = (x + int(w/2)), abs(y - 10)
            cv2.putText(frame, result['label'], label_position , cv2.FONT_HERSHEY_SIMPLEX,1, (255,0,0), 3)

        cv2.imshow("Objet Detection YOLO", frame)
        if frame_number == 240:
            break
        if cv2.waitKey(1) == 13: #13 is the Enter Key
            break

cap.release()
cv2.destroyAllWindows()

    
