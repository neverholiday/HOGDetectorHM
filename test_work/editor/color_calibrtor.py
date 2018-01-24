import cv2
import numpy as np
import argparse


class ColorCalibrator(object):
    def __init__(self,camera_device):
        self.camera_device = camera_device
    
    def selectDevice(self):
        if(self.camera_device == "/dev/video0"):
            return 0
        elif(self.camera_device == "/dev/video1"):
            return 1

    def colorSpace(self,image,lower_bound,upper_bound):
        image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv,lower_bound,upper_bound)
        res = cv2.bitwise_and(image,image,mask=mask)
        return (mask,res)
    
class Trackbar(object):
    """
        Replace GUI Later
    """
    def __init__(self,winname):
        self.winname = winname

    def nothing(self,x):
        pass

    def createTrackbarHSV(self):
        cv2.createTrackbar("h_low",self.winname,0,179,self.nothing)
        cv2.createTrackbar("h_high",self.winname,0,179,self.nothing)
        cv2.createTrackbar("s_low",self.winname,0,255,self.nothing)
        cv2.createTrackbar("s_high",self.winname,0,255,self.nothing)
        cv2.createTrackbar("v_low",self.winname,0,255,self.nothing)
        cv2.createTrackbar("v_high",self.winname,0,255,self.nothing)

    def getvalueHSV(self):        
        h_low = cv2.getTrackbarPos('h_low',self.winname)
        h_high = cv2.getTrackbarPos('h_high',self.winname)
        s_low = cv2.getTrackbarPos('s_low',self.winname)
        s_high = cv2.getTrackbarPos('s_high',self.winname)
        v_low = cv2.getTrackbarPos('v_low',self.winname)
        v_high = cv2.getTrackbarPos('v_high',self.winname)

        lower = np.array([h_low,s_low,v_low],dtype=np.uint8)
        upper = np.array([h_high,s_high,v_high],dtype=np.uint8)

        return (lower,upper)

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("--device",help = "Select camera device",required = True)
    args = vars(ap.parse_args())
    
    cv2.namedWindow("img",cv2.WINDOW_NORMAL)
    trackbar = Trackbar("img")
    trackbar.createTrackbarHSV()

    color_tool = ColorCalibrator(args["device"])
    camera = color_tool.selectDevice()
    cap = cv2.VideoCapture(camera)
    while True:    
        ret,img = cap.read()
        (lower,upper) = trackbar.getvalueHSV()
        (mask,res) = color_tool.colorSpace(img,lower,upper)    
        stack_image = np.hstack((img,res))
        cv2.imshow("img",stack_image)
        k=cv2.waitKey(5)
        if(k == ord('q')):
            break
    cv2.destroyAllWindows


if __name__ == '__main__':
    main()
