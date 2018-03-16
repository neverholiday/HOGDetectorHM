import cv2
import numpy as np
import time
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-m","--mode",help = "capture image or video",required = True)
ap.add_argument("-n","--name",help = "set name of image folder or video",required = True)
args = vars(ap.parse_args())

########### Global Variable ##############
IMAGE_CAPTURE = 1
VIDEO_CAPTURE = 2

mode_capture = 0
save_frame = 0

if(args["mode"] == "image"):
    if( not os.path.exists(args["name"])):
        os.makedirs(args["name"])
    cv2.namedWindow("img",cv2.WINDOW_NORMAL)
    cv2.namedWindow("capture",cv2.WINDOW_NORMAL)
    mode_capture = IMAGE_CAPTURE

if(args["mode"] == "video"):
    
    cv2.namedWindow("img",cv2.WINDOW_NORMAL)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(args["name"],fourcc,20.0,(640,480))
    mode_capture = VIDEO_CAPTURE

cap = cv2.VideoCapture(1)

while True:
    ret,img = cap.read()
    if ret is True:
        
        if(mode_capture == IMAGE_CAPTURE):
            if(save_frame):
                name_image = str(int(time.time())) + ".jpg"
                dir_image = args["name"]+"/"+name_image
                print "save as :" + dir_image
                cv2.imwrite(dir_image,img)
                cv2.imshow("capture",img)
                save_frame = 0
        
        if(mode_capture == VIDEO_CAPTURE):
            if(save_frame):
                print time.time()
                out.write(img)
                
        
        cv2.imshow("img",img)
        
        k = cv2.waitKey(5)
        if k == ord('q'):
            break
        elif k == ord('s'):
            save_frame = (save_frame + 1) % 2
            print "save as :" + args["name"]

cv2.destroyAllWindows()
