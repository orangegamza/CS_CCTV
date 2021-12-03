# camera
from picamera import PiCamera
# image processing
from PIL import Image
import numpy as np
# sleep() now()
from time import sleep
import datetime
# for removing videos
import os

camera = PiCamera()
camera.resolution = (360, 280)
original = np.asarray(Image.open('/home/pi/pic.jpg'))
videoList = []

def customerExists(org, thres):
    sleep(2)
    
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d %H:%M:%S')
    
    camera.capture(filename + ".jpg")
    img = np.asarray(Image.open(filename + ".jpg"))

    diff = org - img
    if np.sum(diff) > thres: # if customer exists
        camera.start_recording(output = filename + ".h264")
        sleep(200)
        camera.stop_recording()
        
        videoList.append(filename)
        return True
    
    else:
        for video in videoList:
            os.remove(video + ".h264")
        videoList = []
        return False

print(customerExists(original, 30))
