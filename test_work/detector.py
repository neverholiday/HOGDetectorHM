import cv2
import numpy as np
import argparse

class Detector(object):
    def __init__(self):
        pass

    ######### Processing before apply contour ########

    def colorSpace(self,image,lower_bound,upper_bound):
        image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv,lower_bound,upper_bound)
        res = cv2.bitwise_and(image,image,mask=mask)
        return (mask,res)

    def threshold(self,image,lower_bound,upper_bound):
        
        ret,threshold = cv2.threshold(image,upper_bound,lower_bound,cv2.THRESH_BINARY_INV)
        return threshold
    
    def lowPassFilter(self,mask):
        kernel = np.ones((5,5),np.uint8)
        retval,th1 = cv2.threshold(mask.copy(),127,255,cv2.THRESH_BINARY_INV)
        opening = cv2.morphologyEx(th1.copy(), cv2.MORPH_OPEN, kernel)
        retval,th2 = cv2.threshold(opening.copy(),127,255,cv2.THRESH_BINARY_INV)
        return th2

    def lowPassfilterBall(self,mask):
        kernel = np.ones((5,5),np.uint8)
        closing = cv2.morphologyEx(mask.copy(), cv2.MORPH_CLOSE, kernel)
        mask_filtered = cv2.morphologyEx(closing.copy(), cv2.MORPH_OPEN, kernel)
        return mask_filtered

    def locateFieldBounderies(self,mask):
        _,contours,hier = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        maxCnt = max(contours,key=lambda x:cv2.contourArea(x))
        hullPoint = cv2.convexHull(maxCnt)
        cv2.drawContours(mask,[hullPoint],-1,255,-1)
        return (hullPoint,mask)

    def detectCircular(self,cnt):
        peri = cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,0.03*peri,True)
        # print(len(approx))
        if(len(approx)>=7):
            return cnt
        else:
            cnt = []
            return cnt

    
    ######### -------------------------------- ########

    ######### Just show it ! ########
        

class Trackbar(object):
    def __init__(self,winname,mode="Trackbar"):
        self.winname = winname
        self.mode = mode

    def nothing(self,x):
        pass

    def createTrackbarHSV(self):
        if(self.mode == "Trackbar"):
            cv2.createTrackbar("h_low",self.winname,0,179,self.nothing)
            cv2.createTrackbar("h_high",self.winname,0,179,self.nothing)
            cv2.createTrackbar("s_low",self.winname,0,255,self.nothing)
            cv2.createTrackbar("s_high",self.winname,0,255,self.nothing)
            cv2.createTrackbar("v_low",self.winname,0,255,self.nothing)
            cv2.createTrackbar("v_high",self.winname,0,255,self.nothing)
        elif(self.mode == "Static"):
            return

    def getvalueHSV(self,static_value):
        if(self.mode == "Trackbar"):
            h_low = cv2.getTrackbarPos('h_low',self.winname)
            h_high = cv2.getTrackbarPos('h_high',self.winname)
            s_low = cv2.getTrackbarPos('s_low',self.winname)
            s_high = cv2.getTrackbarPos('s_high',self.winname)
            v_low = cv2.getTrackbarPos('v_low',self.winname)
            v_high = cv2.getTrackbarPos('v_high',self.winname)
        elif (self.mode == "Static"):
            h_low,s_low,v_low = static_value[0],static_value[1],static_value[2]
            h_high,s_high,v_high = static_value[3],static_value[4],static_value[5]

            # 83 0 0
            # 179 255 255

        lower = np.array([h_low,s_low,v_low],dtype=np.uint8)
        upper = np.array([h_high,s_high,v_high],dtype=np.uint8)

        return (lower,upper)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--image",help = "directory of image",required = True)
    args = vars(ap.parse_args())


    cv2.namedWindow("image",cv2.WINDOW_NORMAL)
    cv2.namedWindow("mask",cv2.WINDOW_NORMAL)
    cv2.namedWindow("res_field",cv2.WINDOW_NORMAL)
    cv2.namedWindow("th",cv2.WINDOW_NORMAL)
    cv2.namedWindow("mask_ball",cv2.WINDOW_NORMAL)
    cv2.namedWindow("res_ball",cv2.WINDOW_NORMAL)
    cv2.namedWindow("original",cv2.WINDOW_NORMAL)

    trackbar = Trackbar("mask",mode="Static")
    trackbar_ball = Trackbar("mask_ball",mode="Static")
    trackbar.createTrackbarHSV()
    trackbar_ball.createTrackbarHSV()
    
    detect = Detector()

    img = cv2.imread(args["image"])
    img_original = img.copy()
    kernel = np.ones((5,5),np.uint8)

    hc = cv2.CascadeClassifier("../test_subject/model/data_haar_121217_13.xml")

# Field Boundaries -------------------------------------------------------------------------------
    static_color_value = np.array([38,37,25,90,255,255],dtype=np.uint8) # use configobj soon 
    lower,upper = trackbar.getvalueHSV(static_color_value)
    mask,res = detect.colorSpace(img,lower,upper)

    th2 = detect.lowPassFilter(mask)

    hull,mask_field = detect.locateFieldBounderies(th2)

    res_field = cv2.bitwise_and(img,img,mask=mask_field)
    cv2.drawContours(img,[hull],-1,(0,0,255),2)
# -------------------------------------------------------------------------------------------------
    # footballs = hc.detectMultiScale(res_field,1.3,10)

    static_color_ball = np.array([83,0,0,179,255,255],dtype=np.uint8)
    lower_ball,upper_ball = trackbar_ball.getvalueHSV(static_color_ball)
    mask_ball,res_ball = detect.colorSpace(res_field,lower_ball,upper_ball)

    filter_mask_ball = detect.lowPassfilterBall(mask_ball)

    a,contours,hierr = cv2.findContours(filter_mask_ball,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img,contours,-1,(255,0,0),2)
    for c in contours:

        circle_contour = detect.detectCircular(c)
        if(len(circle_contour)>0):    
            M = cv2.moments(circle_contour)
            cX = int(M["m10"]/M["m00"])
            cY = int(M["m01"]/M["m00"])
            # cv2.drawContours(img,[circle_contour],-1,(255,0,0),2)
            # ROI
            x_c,y_c,w_c,h_c = cv2.boundingRect(c)
            # cv2.rectangle(img,(x_c,y_c),(x_c+w_c,y_c+h_c),(0,255,0),8)
            cv2.rectangle(img,(cX-100,cY-100),(cX+100,cY+100),(255,0,255),5)
            cv2.circle(img,(cX,cY),10,(255,0,255),-1)
    
    x_start = max(x_c - 20,0) 
    x_end = min(x_c + w_c + 20,img.shape[1])
    y_start = max(y_c - 20,0) 
    y_end = min(y_c + h_c+20,img.shape[0])

    img_roi = img_original[x_start:x_end,y_start:y_end]
    footballs_roi = hc.detectMultiScale(img_roi,1.3,10)

    for (x,y,w,h) in footballs_roi:
        positionX = x+w/2
        positionY = y+h/2
        cv2.circle(img_roi,(positionX,positionY),w/2,(255,0,0),5)
    
    cv2.imshow("original",img_original)
    cv2.imshow("image",img)
    cv2.imshow("mask",mask_field)
    cv2.imshow("th",th2)
    cv2.imshow("res_field",res_field)
    cv2.imshow("mask_ball",filter_mask_ball)
    cv2.imshow("res_ball",res_ball)
    cv2.imshow("ROI",img_roi)
    k = cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()