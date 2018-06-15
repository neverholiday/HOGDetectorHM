import cv2
import argparse
import numpy as np
from detector import Detector

def crop_boundary(img,x,y,w,h):
    x_start = max(x - 30,0) 
    x_end = min(x + w + 30,img.shape[1])
    y_start = max(y - 30,0) 
    y_end = min(y + h + 30,img.shape[0])
    return (x_start,x_end,y_start,y_end)

is_pause = 1
# use_white_select = int(args["mode"])

detector = Detector()
# lower_field = np.array([41,59,53],dtype=np.uint8)
# upper_field = np.array([61,242,255],dtype=np.uint8)
# lower_ball = np.array([0,0,132],dtype=np.uint8)
# upper_ball = np.array([179,42,255],dtype=np.uint8)
lower_field = np.array([36,27,19],dtype=np.uint8)
upper_field = np.array([67,241,237],dtype=np.uint8)
lower_ball = np.array([0,0,140],dtype=np.uint8)
upper_ball = np.array([179,41,255],dtype=np.uint8)


cap = cv2.VideoCapture(1)
# cap = cv2.VideoCapture('../test_subject/video/test_landmark2.avi')
hc = cv2.CascadeClassifier("../test_subject/model/data_haar_2018143_13.xml")
img_roi = np.zeros((50,50),dtype=np.uint8)

while True: 

    # img = cv2.imread(args["image"])
    if(is_pause):
        ret,img = cap.read()
        
    if ret:

        # ---------------------------  Field bouderies ------------------------
    
        mask_zeros = 255*np.ones((img.shape[0],img.shape[1]),dtype=np.uint8)
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        mask_field,_res = detector.colorSpace(img,lower_field,upper_field)
        blur_mask = cv2.GaussianBlur(mask_field,(5,5),0)

        mask_close = cv2.morphologyEx(blur_mask,cv2.MORPH_CLOSE,np.ones((10,10),np.uint8),iterations=1)
        mask_open = cv2.morphologyEx(mask_close,cv2.MORPH_OPEN,np.ones((10,10),np.uint8),iterations=1)

        # mask_dilate = cv2.dilate(mask_erode,np.ones((5,5),dtype=np.uint8))
        ret_th,th1 = cv2.threshold(mask_open,127,255,cv2.THRESH_BINARY)
        ret_th_inv,th_inv = cv2.threshold(th1,127,255,cv2.THRESH_BINARY_INV)
        edge = cv2.Canny(th1,100,200) 

        _c,contours,_hier = cv2.findContours(th_inv,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        # print contours
        img_contours = img.copy()
        if(len(contours)):
            maxCnt = max(contours,key=lambda x: cv2.contourArea(x))
            hull = cv2.convexHull(maxCnt)
            cv2.drawContours(img_contours,[maxCnt],-1,(255,0,0),3)
            cv2.drawContours(mask_zeros,[hull],-1,0,-1)
            finalfield = cv2.bitwise_and(img,img,mask=mask_zeros)

        mask_stack = np.hstack((mask_field,blur_mask,mask_close,mask_open))

        cv2.imshow("zeros",mask_zeros)

    # ---------------------------  Field bouderies ------------------------
        mask_ball,_resball = detector.colorSpace(img,lower_ball,upper_ball)
        mask_and = cv2.bitwise_and(mask_zeros,mask_ball)
        
        _cball,contours_ball,_hierball = cv2.findContours(mask_and,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        ball_contour = img.copy()
        
        for cnt in contours_ball:
            x,y,w,h = cv2.boundingRect(cnt)
            # area_bounding_box = w*h
            if 0.8 <= float(float(w)/float(h)) <= 1.2 and w*h > 100:
                cv2.rectangle(ball_contour,(x,y),(x+w,y+h),(0,0,255),3)
                (x_start,x_end,y_start,y_end) = crop_boundary(img,x,y,w,h)
                img_roi = img[y_start:y_end,x_start:x_end]

                footballs = hc.detectMultiScale(img_roi,1.1,3)
                if len(footballs) > 0:
                    centroid_x=x+w/2
                    centroid_y=y+h/2
                    cv2.circle(ball_contour,(centroid_x,centroid_y),w/2,(255,0,0),2)
            # peri = cv2.arcLength(cnt,True)
            # approx = cv2.approxPolyDP(cnt,0.03*peri,True)
            
            # cv2.drawContours(ball_contour,[cnt],-1,(0,0,255),2)
        
        mask_stack_ball = np.hstack((mask_ball,mask_and))
        cv2.imshow("ball",mask_stack_ball)
        cv2.imshow("ball_contours",ball_contour)
        cv2.imshow("ROI",img_roi)


        cv2.imshow("img",img)
        
        k = cv2.waitKey(10)
        if(k == ord('q')):
            break
        elif(k == ord('p')):
            is_pause = (is_pause+1)%2
            print 'pause'
    else:
        cap.set(cv2.CAP_PROP_POS_MSEC,0)
cap.release()
cv2.destroyAllWindows()
