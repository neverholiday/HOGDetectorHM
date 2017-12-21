import cv2
import numpy as np
import argparse
from test_util import ImageTools

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="Path to image directory")
args = vars(ap.parse_args())

imageDir = args["image"]

image = ImageTools(imageDir)
img = image.matImage()
image.showImage(img)