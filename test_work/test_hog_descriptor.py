import cv2
import numpy as np
from skimage import feature
from skimage import exposure
from test_util import ImageTools

# 1st we should normalize pixel or no normalize before put image to calculate in next step
# No normalize or squre-root normalization (normalize mathod suggestion from 
# https://gurus.pyimagesearch.com/lesson-sample-histogram-of-oriented-gradients-and-car-logo-recognition/?email=hy.nasrun@gmail.com)
# UPDATE : skimage.feature.hog can assign parameter about Normalization 


class testHOGDescriptor(object):
    def __init__(self,matgray_image):
        self.img = matgray_image
    
    def findImageGradient(self):
        img32 = np.float32(self.img) / 255
        sobelX = cv2.Sobel(img32,cv2.CV_32F,1,0,ksize=1)
        sobelY = cv2.Sobel(img32,cv2.CV_32F,0,1,ksize=1)
        mag,angle = cv2.cartToPolar(sobelX,sobelY,angleInDegrees=True)
        return mag

    def extractHOG(self):
        (H,hogImage) = feature.hog(self.img,orientations=9,pixels_per_cell=(10,10),
        cells_per_block=(2, 2),transform_sqrt=True,visualise=True)
        hogImage = exposure.rescale_intensity(hogImage,out_range=(0, 255))
        hogImage = hogImage.astype("uint8")
        return hogImage

def main():
    imageDir = "../test_subject/crop_output/football5.jpg"

    imTool = ImageTools(imageDir)
    img = imTool.matImageGray()

    descriptor = testHOGDescriptor(img)
    
    imgGradient = descriptor.findImageGradient()

    imgExtract = descriptor.extractHOG()

    imTool.showImage(imgGradient,"image")
    imTool.showImage(imgExtract,"test")

    imTool.breakWindows()

if __name__ == '__main__':
    main()
