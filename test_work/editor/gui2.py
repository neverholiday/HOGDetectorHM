import sys
from PyQt4 import QtCore, QtGui, uic
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--ui",help = "Select UI File from qt designer",required = True)
args = vars(ap.parse_args())

qtCreatorFile = args["ui"] # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.calculate.clicked.connect(self.Calculate)
    
    def Calculate(self):
        price = int(self.textEdit.toPlainText())
        tax = (self.spinBox.value())

        total_price = price + (10*tax)
        total_price_string = "Paid : " + str(total_price)
        self.result.setText(total_price_string)
        
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())