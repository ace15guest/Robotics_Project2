#Object detection
import cv2
#Display 
from IPython.display import display
#Jetbot Camera 
from jetbot import Camera, bgr8_to_jpeg
#Widgets
import ipywidgets.widgets as widgets
#
import traitlets
#
from jetbot import Robot
#
import os 
#
from uuid import uuid1
#
from PIL import Image

import cv2
import numpy as np
from IPython.display import display, Image
import ipywidgets as widgets
import threading
import time
from jetbot import Robot


robot = Robot()



cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),width=640,height=480,framerate=30/1,format=NV12 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)
def find_face(img):
    img_name = str(uuid1())
    save_dir = os.getcwd()+'/'+ img_name +'.jpg' #saving image
    with open(save_dir, 'wb') as photo:
        photo.write(img.value)
    img_1 = cv2.imread(save_dir) #reading image
    os.remove(save_dir)
    img_gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB)
    stop_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    found = stop_data.detectMultiScale(img_gray, 
                                   minSize =(20, 20))
    amount_found = len(found)
    
    if amount_found != 0:
        # There may be more than one
        # sign in the image
        for (x, y, width, height) in found:

            # We draw a green rectangle around
            # every recognized sign
            img_1=cv2.rectangle(img_rgb, (x, y), (x + height, y + width), (0, 255, 0), 5)
            print (x,y)
            
            display(Image.fromarray(img_1))
            return x, y
   #Creating a Stop Button
#https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html

stopButton = widgets.ToggleButton(
    value=False,
    description='Stop',
    disabled=False,
    button_style='danger', 
    tooltip='Description',
    icon='square' 
)
########################################
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Display function
# ================
def view(button):
    cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),width=640,height=480,framerate=30/1,format=NV12 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)
    display_handle=display(None, display_id=True)
    i = 0
    leftcount=0
    rightcount=0
    forwardscount=0
    backwardscount=0

    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1) # if your camera reverses your image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if faces != ():
            (x, y, w, h) = faces[0]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

##########################################
#######turning left and right######################

            i=i+1
            x0=240
            if x-x0<-30:
                direction='right'
                rightcount=rightcount+1
    #                 distance=x-x0
            if x-x0>30:
                direction='left'
                leftcount=leftcount+1
    #                 distance=x0-x

            if leftcount>2:
                robot.backward(0.3)
                time.sleep(.2)
                robot.stop()
                leftcount=0
                rightcount=0
                print(direction)
            if rightcount>2:
                robot.forward(0.3)
                time.sleep(.2)
                robot.stop()
                rightcount=0
                leftcount=0

########################################
#######turning forward and backward######################
        
            w0=100
            if w-w0>0:
                #backwards=left
                direction='backwards'
                backwardscount=backwardscount+1
            if w-w0<0:
                direction='forwards'
                forwardscount=forwardscount+1
            if backwardscount>5:
                robot.left(0.3)
                time.sleep(.5)
                robot.stop()
                backwardscount=0
                forwardscount=0
                print(direction)
            if forwardscount>5:
                robot.right(0.3)
                time.sleep(.5)
                robot.stop()
                backwardscount=0
                forwardscount=0
      
            
########################################################

        _, frame = cv2.imencode('.jpeg', frame)
        
        display_handle.update(Image(data=frame.tobytes()))
        if stopButton.value==True:
            cap.release()
            robot.stop()
            display_handle.update(None)

            
# Run
# ================
display(stopButton)
thread = threading.Thread(target=view, args=(stopButton,))
thread.start()
