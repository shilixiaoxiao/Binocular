# -*- coding: utf-8 -*-
"""

Created on 2021/6/10
@author: Jimmy
"""
import sys

from PyQt5.QtWidgets import QApplication , QMainWindow
from PyQt5 import QtGui
from run import Run

if __name__=="__main__":
    app = QApplication(sys.argv)
    myWin = Run()
    myWin.show()
    sys.exit(app.exec_())
