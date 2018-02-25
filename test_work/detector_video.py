import cv2
import argparse
import numpy as np
from detector import Detector

# ap = argparse.ArgumentParser()
# ap.add_argument("-i","--image",help="directory of image",required=True)
# args = vars(ap.parse_args())

detector = Detector()
lower_field = np.array([33,40,56],dtype=np.uint8)
upper_field = np.array([58,255,255],dtype=np.uint8)
lower_ball = np.array([0,0,67],dtype=np.uint8)
upper_ball = np.array([179,73,255],dtype=np.uint8)

cap = cv2.VideoCapture(1)
hc = cv2.CascadeClassifier("../test_subject/model/data_haar_121217_13.xml")

while True: 

    # img = cv2.imread(args["image"])
    ret,img = cap.read()

    # Field bouderies

    mask_field,_res = detector.colorSpace(img,lower_field,upper_field)
    th_field = detector.lowPassFilter(mask_field)
    hull,mask_field_after_filter = detector.locateFieldBounderies(th_field)

    res_field = cv2.bitwise_and(img,img,mask=mask_field_after_filter)

    # detect white object

    mask_ball,res_ball = detector.colorSpace(res_field,lower_ball,upper_ball)
    mask_ball_after_filter = detector.lowPassfilterBall(mask_ball)

    _,contours,hierr = cv2.findContours(mask_ball_after_filter,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        circle_contour = detector.detectCircular(c)
        if(len(circle_contour)>0):
            M = cv2.moments(circle_contour)
            cX = int(M["m10"]/M["m00"])
            cY = int(M["m01"]/M["m00"])
            # cv2.drawContours(img,[circle_contour],-1,(255,0,0),2)
            
            # ROI
            x,y,w,h = cv2.boundingRect(c)
            if ( 0.9<= float(w)/float(h) <= 1.2):
                
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                x_start = max(x - 20,0) 
                x_end = min(x + w + 20,img.shape[1])
                y_start = max(y - 20,0) 
                y_end = min(y + h + 20,img.shape[0])

                img_roi = img[y_start:y_end,x_start:x_end]
                footballs_roi = hc.detectMultiScale(img_roi,1.3,10)
                print footballs_roi
                if len(footballs_roi) >= 1:
                    positionX = x+w/2
                    positionY = y+h/2
                    cv2.circle(img,(positionX,positionY),w/2,(255,0,0),5)

                # for (x,y,w,h) in footballs_roi:
                #     positionX = x+w/2
                #     positionY = y+h/2
                #     cv2.circle(img,(positionX,positionY),w/2,(255,0,0),5)

            # cv2.rectangle(img,(cX-100,cY-100),(cX+100,cY+100),(255,0,255),5)
            # cv2.circle(img,(cX,cY),10,(255,0,255),-1)

    cv2.imshow("img",img)
    cv2.imshow("field boudery",res_field)
    cv2.imshow("mask ball",mask_ball_after_filter)

    k = cv2.waitKey(10)
    if(k == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
