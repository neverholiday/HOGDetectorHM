# crop created by chattarin

import cv2
import numpy as np
import os
import argparse
import time

ap = argparse.ArgumentParser()
ap.add_argument("-i","--input",help = "input image for crop",required = True)
ap.add_argument("-o","--output",help = "output directory",required = True)
ap.add_argument("-m","--mode",help = "select Mode crop hard negative")
argument = vars(ap.parse_args())

STATEMouse = False
STATECrop = False
_previousX = 0
_previousY = 0
_currentX = 0
_currentY = 0

index = 0

# "../image"
directory_image = argument["input"] 
directory_output = argument["output"]
path_xml = '../xml_file/data_haar111217_2.xml'


cv2.namedWindow("image",cv2.WINDOW_NORMAL)
cv2.namedWindow("crop",cv2.WINDOW_NORMAL)

if(argument["mode"] == "crop_negative"):
    cv2.namedWindow("negative",cv2.WINDOW_NORMAL)

if(argument["mode"] == "directory_input"):
    list_dir = os.listdir(directory_image)
    number_list = len(list_dir)
    img = cv2.imread(directory_image+"/"+list_dir[0],0)
    img_ = img.copy()
    img_2 =  img.copy()

else:
    img = cv2.imread(directory_image,0)
    img_ = img.copy()
    img_2 =  img.copy()

def _callBackLeftClick(event,x,y,flags,param):
    global _previousX,_previousY,STATEMouse,STATECrop,img_,img,img_2,_currentX,_currentY
    if event == cv2.EVENT_LBUTTONDOWN:
        # cv2.destroyWindow("crop")
        STATEMouse = True
        STATECrop = False
        _previousX,_previousY = x,y
        img_ = img.copy()
    elif event == cv2.EVENT_MOUSEMOVE :
        if STATEMouse is True:
            img_ = img.copy()
            _currentX,_currentY = x,y
            cv2.rectangle(img_,(_previousX,_previousY),(x,y),(255,255,255),3)
    elif event == cv2.EVENT_LBUTTONUP:
        STATEMouse = False
        STATECrop = True        
        cv2.rectangle(img_,(_previousX,_previousY),(x,y),(255,255,255),3)

def haarDetect(img):
    
    hc = cv2.CascadeClassifier(path_xml)
    footballs = hc.detectMultiScale(img)
    
    return footballs


def main():
    global img,img_,index
    if(argument["mode"] == "directory_input"):
        global number_list
        number_list -= 1
    if(argument["mode"] == "crop_negative"):
        img_circle = img.copy()
        footballs = haarDetect(img)
        for(x,y,w,h) in footballs:
            positionX = x+w/2
            positionY = y+h/2
            cv2.circle(img_circle,(positionX,positionY),w/2,(255,255,255),3)

    cv2.setMouseCallback("image",_callBackLeftClick)
    while True:
        # img_ = img.copy()
        if STATECrop:
            cv2.imshow("crop",img[_previousY:_currentY,_previousX:_currentX])
            # print img[_previousY:_currentY,_previousX:_currentX].shape


        cv2.imshow("image",img_)
        if(argument["mode"] == "crop_negative"):
            cv2.imshow("negative",img_circle)
        k = cv2.waitKey(5)
        if(k == ord('q')):
            break
        elif (k == ord('c')):
            img = cv2.imread("../image/ball0.jpg",0)
        elif (k == ord('x')):
            name_image = str(int(time.time())) + ".jpg"
            print "save as",directory_output+"/"+name_image
            save_image = img[_previousY:_currentY,_previousX:_currentX].copy()
            save_image = cv2.resize(save_image,(200,200))
            cv2.imwrite(directory_output+"/"+name_image,save_image)
        elif (k == ord('d')):
            index += 1 
            number_list -= 1
            print "remaining" + str(number_list)
            img = cv2.imread(directory_image+list_dir[index],0)
            img_ = img.copy()
            img_2 =  img.copy()
            
            
    cv2.destroyAllWindows()
    

if __name__ == '__main__':

    main()
    
