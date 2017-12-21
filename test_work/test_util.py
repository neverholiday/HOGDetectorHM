import cv2
import numpy as np

class ImageTools(object):
    def __init__(self,directory_image):
        self.dir = directory_image
    
    def matImage(self):
        return cv2.imread(self.dir)

    def matImageGray(self):
        return cv2.imread(self.dir,0)

    def showImage(self,matImage,nameWindow):
        cv2.namedWindow(nameWindow)
        cv2.imshow(nameWindow,matImage)
    
    def breakWindows(self,mode="image"):
        if mode == "image":
            cv2.waitKey(0)
        elif mode == "video":
            k = cv2.waitKey(5)
            return k
        cv2.destroyAllWindows()

def main():
    imageDir = "../test_subject/football_image/1.jpg"

    image = ImageTools(imageDir)

    img = image.matImageGray()
    image.showImage(img)

if __name__ == '__main__':
    main()