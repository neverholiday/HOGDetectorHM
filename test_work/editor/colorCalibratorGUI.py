#!/usr/bin/env python
import cv2
import numpy as np

from PyQt4 import QtCore, QtGui

from colorGUI import Ui_ColorCalibrator
from colorCalibrator import ColorCalibrator


try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class mainUI(Ui_ColorCalibrator):
	def __init__(self,qtgui):
		self.setupUi(qtgui)
		# self.color_calibrate = ColorCalibrator()
		self.capture = None
		self.cameraID = None
		self.configFile = None
		self.image = None
		self.__res = None
		self.__list_hsv = [0,0,0,0,0,0]
		self.colorSpace = ColorCalibrator()

		self.cameraButton.clicked.connect(self._initCamera)
		self.saveButton.clicked.connect(self._saveConfig)
		self.HLow.valueChanged.connect(self._getHSVValue)
		self.SLow.valueChanged.connect(self._getHSVValue)
		self.VLow.valueChanged.connect(self._getHSVValue)
		self.HUpper.valueChanged.connect(self._getHSVValue)
		self.SUpper.valueChanged.connect(self._getHSVValue)
		self.VUpper.valueChanged.connect(self._getHSVValue)

	# def showCamera(self):
	# 	self._initCamera()

	def _initCamera(self):
		if self.cameraComboBox.currentText() == "Webcam":
			print "Using Webcam"
			self.cameraID = 0
		elif self.cameraComboBox.currentText() == "ExternalCamera":
			print "Using External Camera"
			self.cameraID = 1
		self.capture = cv2.VideoCapture(self.cameraID)
		# self.capture = cv2.VideoCapture(0)
		self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
		self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self._updateFrame)
		self.timer.start(20)

	def _updateFrame(self):
		ret,self.image = self.capture.read()

		lowerBound = self.__list_hsv[3:6]
		upperBound = self.__list_hsv[0:3]

		(mask,self.__res) = self.colorSpace.colorSpace(self.image,np.array(lowerBound),np.array(upperBound))

		self.__res = cv2.flip(self.__res,1)
		self._displayImage(self.__res)

	def _displayImage(self,image):

		qformat = QtGui.QImage.Format_RGB888
		OutImage = QtGui.QImage(image,image.shape[1],image.shape[0],image.strides[0],qformat)
		OutImage = OutImage.rgbSwapped()	

		self.imageLable.setPixmap(QtGui.QPixmap.fromImage(OutImage))


	def _saveConfig(self):
		
		print self.namefileEdit.text()
	

	def _getHSVValue(self):
		HSVList = [self.HUpper.value(),
				  self.SUpper.value(),
				  self.VUpper.value(),
				  self.HLow.value(),
				  self.SLow.value(),
				  self.VLow.value()]
		# print HSVList
		self.__list_hsv = HSVList

if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	ColorCalibrator_GUI = QtGui.QMainWindow()
	ui = mainUI(ColorCalibrator_GUI)
	ColorCalibrator_GUI.show()
	sys.exit(app.exec_())

