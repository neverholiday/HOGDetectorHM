import cv2
import numpy as np
import argparse
from configobj import ConfigObj

class ColorCalibrator(object):
    def __init__(self,camera_device):
        self.camera_device = camera_device
    
    def selectDevice(self):
        if(self.camera_device == "/dev/video0"):
            return 0
        elif(self.camera_device == "/dev/video1"):
            return 1
        else:
            return self.camera_device

    def colorSpace(self,image,lower_bound,upper_bound):
        image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv,lower_bound,upper_bound)
        res = cv2.bitwise_and(image,image,mask=mask)
        return (mask,res)
    
    def createConfig(self,path,list_hsv):
        config = ConfigObj(indent_type='\t')
        config['ColorDefinitions'] = {}
        config['ColorDefinitions']['OrangeColorParameter'] = {'ID':'1',
                                                                'Name':'orange',
                                                                'RenderColor_RGB':'(255, 128, 0)',
                                                                'MinArea_pixels':'4',
                                                                
                                                                'H_Max':'0',
                                                                'H_Min':'0',
                                                                'S_Max':'0',
                                                                'S_Min':'0',
                                                                'V_Max':'0',
                                                                'V_Min':'0'}
        
        config['ColorDefinitions']['FieldGreenColorParameter'] = {'ID':'2',
                                                                    'Name':'green',
                                                                    'RenderColor_RGB':'(0, 128, 0)',
                                                                    'MinArea_pixels':'4',
                                                                    
                                                                    'H_Max':str(list_hsv[3]),
                                                                    'H_Min':str(list_hsv[0]),
                                                                    'S_Max':str(list_hsv[4]),
                                                                    'S_Min':str(list_hsv[1]),
                                                                    'V_Max':str(list_hsv[5]),
                                                                    'V_Min':str(list_hsv[2])}

        config['ColorDefinitions']['BlueColorParameter'] = {'ID':'3',
                                                                'Name':'blue',
                                                                'RenderColor_RGB':'(0, 0, 255)',
                                                                'MinArea_pixels':'4',
                                                                
                                                                'H_Max':'0',
                                                                'H_Min':'0',
                                                                'S_Max':'0',
                                                                'S_Min':'0',
                                                                'V_Max':'0',
                                                                'V_Min':'0'}

        config['ColorDefinitions']['YellowColorParameter'] = {'ID':'4',
                                                                'Name':'yellow',
                                                                'RenderColor_RGB':'(255, 255, 0)',
                                                                'MinArea_pixels':'4',
                                                                
                                                                'H_Max':'0',
                                                                'H_Min':'0',
                                                                'S_Max':'0',
                                                                'S_Min':'0',
                                                                'V_Max':'0',
                                                                'V_Min':'0'}

        config['ColorDefinitions']['WhiteColorParameter'] = {'ID':'5',
                                                                'Name':'white',
                                                                'RenderColor_RGB':'(255, 255, 255)',
                                                                'MinArea_pixels':'4',
                                                                
                                                                'H_Max':'0',
                                                                'H_Min':'0',
                                                                'S_Max':'0',
                                                                'S_Min':'0',
                                                                'V_Max':'0',
                                                                'V_Min':'0'}

        config['ColorDefinitions']['BlackColorParameter'] = {'ID':'6',
                                                                'Name':'black',
                                                                'RenderColor_RGB':'(100, 100, 100)',
                                                                'MinArea_pixels':'4',
                                                                
                                                                'H_Max':'0',
                                                                'H_Min':'0',
                                                                'S_Max':'0',
                                                                'S_Min':'0',
                                                                'V_Max':'0',
                                                                'V_Min':'0'}

        config['ColorDefinitions']['MagentaColorParameter'] = {'ID':'7',
                                                                'Name':'magenta',
                                                                'RenderColor_RGB':'(255, 0, 128)',
                                                                'MinArea_pixels':'4',
                                                                
                                                                'H_Max':'0',
                                                                'H_Min':'0',
                                                                'S_Max':'0',
                                                                'S_Min':'0',
                                                                'V_Max':'0',
                                                                'V_Min':'0'}
                                                                
        config['ColorDefinitions']['CyanColorParameter'] = {
                                                            'ID':'8',
                                                            'Name':'cyan',
                                                            'RenderColor_RGB':'(0, 255, 255)',
                                                            'MinArea_pixels':'4',
                                                            
                                                            'H_Max':'0',
                                                            'H_Min':'0',
                                                            'S_Max':'0',
                                                            'S_Min':'0',
                                                            'V_Max':'0',
                                                            'V_Min':'0'
                                                            }
        config['CameraParameters'] = {}
        config.filename = path
        config.write()
    
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
    ap.add_argument("--config",help = "Directory and Name of config file")
    args = vars(ap.parse_args())

    is_pause = 1

    cv2.namedWindow("img",cv2.WINDOW_NORMAL)
    trackbar = Trackbar("img")
    trackbar.createTrackbarHSV()

    color_tool = ColorCalibrator(args["device"])
    camera = color_tool.selectDevice()
    cap = cv2.VideoCapture(camera)
    print cap.get(cv2.CAP_PROP_AUTOFOCUS)
    print cap.get(cv2.CAP_PROP_BRIGHTNESS)
    # print cap.get(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U)
    # print cap.get(cv2.CAP_PROP_WHITE_BALANCE_RED_V)
    
    while True:   
        if(is_pause): 
            ret,img = cap.read()
        if ret:
            (lower,upper) = trackbar.getvalueHSV()
            (mask,res) = color_tool.colorSpace(img,lower,upper)    
            stack_image = np.hstack((img,res))
            cv2.imshow("img",stack_image)
            k=cv2.waitKey(5)
            if(k == ord('q')):
                break
            elif(k==ord('p')):
                print 'pause'
                is_pause = (is_pause + 1)%2
            elif(k==ord('r')):
                cap.set(cv2.CAP_PROP_POS_MSEC,0)
            elif(k==ord('s')):
                hsv_list = np.hstack((lower,upper))
                print 'Save as ..' + args["config"]
                color_tool.createConfig(args["config"],hsv_list)
        else:
            cap.set(cv2.CAP_PROP_POS_MSEC,0)

    cv2.destroyAllWindows


if __name__ == '__main__':
    main()
