import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from gui2 import TestGUI

class AppWindow(QDialog):
    def __init__(self):
        super.__init__()
        self.ui = TestGUI()
        self.ui.setupUi(self)
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())