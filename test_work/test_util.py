import cv2
import numpy as np
import argparse

class ImageTools(object):
    def __init__(self,directory_image,nameWindow):
        self.dir = directory_image
        self.nameWindow = nameWindow
        cv2.namedWindow(nameWindow,cv2.WINDOW_NORMAL)

    def matImage(self):
        return cv2.imread(self.dir)

    def matImageGray(self):
        return cv2.imread(self.dir,0)
    
    def imageHSV(self,image):
        return cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    def maskHSV(self,image,image_hsv,lower_bound,upper_bound):
        mask = cv2.inRange(image_hsv,lower_bound,upper_bound)
        res = cv2.bitwise_and(image,image,mask=mask)
        return (mask,res)

    def stackImage(self,tuple_image):
        mask_three = np.zeros((tuple_image[0].shape[0],tuple_image[0].shape[1],3),dtype=np.uint8)
        mask_three[:,:,0] = tuple_image[1]
        mask_three[:,:,1] = tuple_image[1]
        mask_three[:,:,2] = tuple_image[1]                
        
        new_tuple = (tuple_image[0],mask_three,tuple_image[2],tuple_image[3])

        return np.hstack(new_tuple)

    def showImage(self,matImage):
        cv2.imshow(self.nameWindow,matImage)
    
    def breakWindows(self,mode="image"):
        if mode == "image":
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif mode == "video":
            k = cv2.waitKey(5)
            return k

    def nothing(self,x):
        pass
    
    def createTrackbarHSV(self):
        cv2.createTrackbar("h_low",self.nameWindow,0,179,self.nothing)
        cv2.createTrackbar("h_high",self.nameWindow,0,179,self.nothing)
        cv2.createTrackbar("s_low",self.nameWindow,0,255,self.nothing)
        cv2.createTrackbar("s_high",self.nameWindow,0,255,self.nothing)
        cv2.createTrackbar("v_low",self.nameWindow,0,255,self.nothing)
        cv2.createTrackbar("v_high",self.nameWindow,0,255,self.nothing)
    
    def getvalueHSV(self,mode="Trackbar"):
        if(mode == "Trackbar"):
            h_low = cv2.getTrackbarPos('h_low',self.nameWindow)
            h_high = cv2.getTrackbarPos('h_high',self.nameWindow)
            s_low = cv2.getTrackbarPos('s_low',self.nameWindow)
            s_high = cv2.getTrackbarPos('s_high',self.nameWindow)
            v_low = cv2.getTrackbarPos('v_low',self.nameWindow)
            v_high = cv2.getTrackbarPos('v_high',self.nameWindow)
        elif(mode == "Static"):
            h_low,s_low,v_low = 85,71,171
            h_high,s_high,v_high = 179,255,255

            

        lower = np.array([h_low,s_low,v_low],dtype=np.uint8)
        upper = np.array([h_high,s_high,v_high],dtype=np.uint8)

        return (lower,upper)


def argumentParse():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--image",help = "directory of image",required = True)
    args = vars(ap.parse_args())
    return args

def main():
    arg =  argumentParse()
    imageDir = arg["image"]
    # instance of general image tools
    image = ImageTools(imageDir,"image")
    image.createTrackbarHSV()

    while(True):
        img = image.matImage()

        img_hsv = image.imageHSV(img)

        # lower_bound,upper_bound = image.getvalueHSV(mode="Static")
        lower_bound,upper_bound = image.getvalueHSV(mode="Trackbar")
        # 85,71,171 : 179,255,255

        mask_image,res_image = image.maskHSV(img,img_hsv,lower_bound,upper_bound)

        _,contours,_ = cv2.findContours(mask_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        img_white = 255 * np.ones((img.shape[0],img.shape[1],3),dtype=np.uint8)
        cv2.drawContours(img_white,contours,-1,(0,0,0),1)
        
        tuple_image = (img,mask_image,res_image,img_white)
        stack_image = image.stackImage(tuple_image)
        image.showImage(stack_image)
        k = image.breakWindows("video")
        if(k == ord('q')):
            break
    # print len(contours)
    # for cnt in contours:
    #     area = cv2.contourArea(cnt)
    #     print area
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()