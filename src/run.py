# -*- coding: utf-8 -*-
"""

Created on 2021/6/10
@author: Jimmy
"""

import numpy as np
import cv2
import glob
import sys

from stereo_calibration import calibration
from shift_calculate import calculate
from binocular import Ui_MainWindow
from PyQt5.QtWidgets import QApplication , QMainWindow
from PyQt5 import QtGui

class Run(QMainWindow , Ui_MainWindow):
    def __init__(self,parent = None):
        super(Run,self).__init__(parent)
        self.setupUi(self)
        self.calc = calculate()
        self.cali = calibration()
        self.capture_calibration_Btn.clicked.connect(self.capture_calibration)
        self.binocular_calibration_Btn.clicked.connect(self.binocular_calibration)
        self.capture_calculate_Btn.clicked.connect(self.capture_and_calculate_1frame)
        self.continue_calculate_Btn.clicked.connect(self.continue_capture_calculate)

    def capture_calibration(self):
        self.cali.capture_calibration()

    def binocular_calibration(self):
        self.cali.binocular_calibration()

    def capture_and_calculate_1frame(self):
        self.calc.capture_1_frame()
        self.load_img()
        self.calc.remap()

    def continue_capture_calculate(self):
        while(1):
            self.calc.auto_get_1_frame()
            self.calc.get_tmp_img()
            self.calc.shift_calc()

    def load_img(self):
        tmp_img_left = cv2.imread("../left_tmp/left_tmp.jpg")
        tmp_img_right = cv2.imread("../right_tmp/right_tmp.jpg")
        tmp_img_left = cv2.cvtColor(tmp_img_left,cv2.COLOR_BGR2RGB)
        tmp_img_right = cv2.cvtColor(tmp_img_right,cv2.COLOR_BGR2RGB)
        _img_left = QtGui.QImage(tmp_img_left[:],tmp_img_left.shape[1],tmp_img_left.shape[0],
                                 tmp_img_left.shape[1]*3,QtGui.QImage.Format_RGB888)
        _img_right = QtGui.QImage(tmp_img_right[:],tmp_img_right.shape[1],tmp_img_right.shape[0],
                                 tmp_img_right.shape[1]*3,QtGui.QImage.Format_RGB888)
        out_left = QtGui.QPixmap(_img_left).scaled(self.left_frame.width(),self.left_frame.height())
        out_right = QtGui.QPixmap(_img_right.scaled(self.right_frame.width(),self.right_frame.height()))
        self.left_frame.setPixmap(out_left)
        self.right_frame.setPixmap(out_right)

    #cali.capture_calibration()
    #cali.binocular_calibration()
    #calc.capture_1_frame()
    #calc.remap()

    # while(1):
    #     calc.auto_get_1_frame()
    #
    #     calc.get_tmp_img()
    #     calc.shift_calc()

if __name__=="__main__":
    app = QApplication(sys.argv)
    myWin = Run()
    myWin.show()
    sys.exit(app.exec_())


