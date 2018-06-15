import cv2
import numpy as np
from detector import Detector

class BallFinder(object):
    
    def __init__(self,boundary = None):
        self.boundary = boundary
        