from configobj import ConfigObj
import numpy as np
import cv2
from detector import Detector
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help = "input video landmark test",required = True)
argument = vars(ap.parse_args())

color_detect = Detector()

# path_config = '../test_subject/config_file/colordef_hanuman2.ini'
# config = ConfigObj(path_config)

# h_low = int(config['ColorDefinitions']['FieldGreenColorParameter']['H_Min'])
# h_upper = int(config['ColorDefinitions']['FieldGreenColorParameter']['H_Max'])
# s_low = int(config['ColorDefinitions']['FieldGreenColorParameter']['S_Min'])
# s_upper = int(config['ColorDefinitions']['FieldGreenColorParameter']['S_Max'])
# v_low = int(config['ColorDefinitions']['FieldGreenColorParameter']['V_Min'])
# v_upper = int(config['ColorDefinitions']['FieldGreenColorParameter']['V_Max'])

upper_bound = np.array([106,255,240])
lower_bound = np.array([36,64,14])

upper_land_mark = np.array([14,255,255])
lower_land_mark = np.array([0,81,41])



path_video = argument["video"]
cap = cv2.VideoCapture(path_video)
is_play = 1
while True:
    
    if is_play:
        ret,frame = cap.read()
    
    if ret:

        mask,res = color_detect.colorSpace(frame,lower_bound,upper_bound)
        
        res_after_filter = color_detect.fieldAfterFilter(frame,mask,res)
        
        mask_lm,res_lm = color_detect.colorSpace(frame,lower_land_mark,upper_land_mark)
        mask_lm_after1 = cv2.erode(mask_lm,np.ones((15,15),dtype=np.uint8))
        mask_lm_after_filter = cv2.dilate(mask_lm_after1,np.ones((15,15),dtype=np.uint8))
        
        res_lm_after_filter = cv2.bitwise_and(frame,frame,mask=mask_lm_after_filter)

        _,contours,hierr = cv2.findContours(mask_lm_after_filter,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame,contours,-1,(255,0,0),2)

        cv2.imshow("img",frame)
        cv2.imshow("res",res_after_filter)
        cv2.imshow("res_lm",mask_lm)
        cv2.imshow("res_lm_after_filter",res_lm_after_filter)
        k = cv2.waitKey(20)
        if(k == ord('q')):
            break
        elif(k == ord('p')):
            print 'pause'
            is_play = (is_play + 1) % 2
    else:
        cap.set(cv2.CAP_PROP_POS_MSEC,0)

        
cap.release()
cv2.destroyAllWindows()

