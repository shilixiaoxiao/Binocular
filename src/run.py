# -*- coding: utf-8 -*-
"""

Created on 2021/6/10
@author: Jimmy
"""

import numpy as np
import cv2
import glob
import sys
import os
from stereo_calibration import calibration
from shift_calculate import calculate
from binocular import Ui_MainWindow
from PyQt5.QtWidgets import QApplication , QMainWindow
from PyQt5 import QtGui

class Run(QMainWindow , Ui_MainWindow):
    def __init__(self,parent = None):
        super(Run,self).__init__(parent)
        self.setupUi(self)
        self.cali = calibration()
        self.calc = calculate()
        self.cap0 = self.cali.cap0
        self.cap1 = self.cali.cap1
        self.capture_calibration_Btn.clicked.connect(self.capture_calibration)
        self.binocular_calibration_Btn.clicked.connect(self.binocular_calibration)
        self.capture_calculate_Btn.clicked.connect(self.capture_and_calculate_1frame)
        self.continue_calculate_Btn.clicked.connect(self.continue_capture_calculate)

    def capture_calibration(self):
        n = 0
        while(1):
            ret0, frame0 = self.cap0.read()
            ret1, frame1 = self.cap1.read()
            frame0,frame1 = self.frame_to_display(frame0,frame1)
            #cv2.imshow("capture0",frame0)
            #cv2.imshow("capture1",frame1)
            self.left_frame.setPixmap(frame0)
            self.right_frame.setPixmap(frame1)

            if ret0 == True and ret1 == True:
                k=cv2.waitKey(1)
                if(k == ord("q")):

                    break
                elif(k == ord("p")):
                    if not os.path.exists(self.path_left):
                        os.mkdir(self.path_left)
                    if not os.path.exists(self.path_right):
                        os.mkdir(self.path_right)
                    cv2.imwrite(self.path_left + "/left0" + str(n) + ".jpg", frame0)
                    cv2.imwrite(self.path_right + "/right0" + str(n) + ".jpg", frame1)
                    print(n)
                    n += 1

        self.cap0.release()
        self.cap1.release()
        self.left_frame.clear()
        self.right_frame.clear()
        print("calibration capture finished!")
        # cv2.destroyAllWindows()

    def binocular_calibration(self):
        self.cali.binocular_calibration()

    def capture_and_calculate_1frame(self):
        self.capture_1_frame()
        self.load_img()
        self.calc.remap()

    def capture_1_frame(self):
        cap0 = self.cap0
        cap1 = self.cap1
        while (1):

            ret0, frame0 = cap0.read()
            ret1, frame1 = cap1.read()
            frame0,frame1 = self.frame_to_display(frame0,frame1)
            # cv2.imshow("capture0", frame0)
            # cv2.imshow("capture1", frame1)
            self.left_frame.setPixmap(frame0)
            self.right_frame.setPixmap(frame1)

            if ret0 == True and ret1 == True:
                k = cv2.waitKey(1)
                if (k == ord("q")):
                    break
                elif (k == ord("p")):
                    if not os.path.exists("../left_tmp"):
                        os.mkdir("../left_tmp")
                    if not os.path.exists("../right_tmp"):
                        os.mkdir("../right_tmp")
                    cv2.imwrite("../left_tmp/left_tmp.jpg", frame0)
                    cv2.imwrite("../right_tmp/right_tmp.jpg", frame1)
                    print("capture successed!")

        cap0.release()
        cap1.release()
        self.left_frame.clear()
        self.right_frame.clear()
        self.load_img()
        # cv2.destroyAllWindows()

    def frame_to_display(self,frame0,frame1):
        tmp_img_left = frame0
        tmp_img_right = frame1
        _img_left = QtGui.QImage(tmp_img_left[:], tmp_img_left.shape[1], tmp_img_left.shape[0],
                                 tmp_img_left.shape[1] * 3, QtGui.QImage.Format_RGB888)
        _img_right = QtGui.QImage(tmp_img_right[:], tmp_img_right.shape[1], tmp_img_right.shape[0],
                                  tmp_img_right.shape[1] * 3, QtGui.QImage.Format_RGB888)
        out_left = QtGui.QPixmap(_img_left).scaled(self.left_frame.width(), self.left_frame.height())
        out_right = QtGui.QPixmap(_img_right.scaled(self.right_frame.width(), self.right_frame.height()))
        return out_left,out_right

    def auto_get_1_frame(self):
        ret0, frame0 = self.cap0.read()
        ret1, frame1 = self.cap1.read()
        frame0,frame1 = self.frame_to_display(frame0,frame1)
        # cv2.imshow("capture0", frame0)
        # cv2.imshow("capture1", frame1)
        self.left_frame.setPixmap(frame0)
        self.right_frame.setPixmap(frame1)
        if ret0 == True and ret1 == True:
            if not os.path.exists("../left_tmp"):
                os.mkdir("../left_tmp")
            if not os.path.exists("../right_tmp"):
                os.mkdir("../right_tmp")
            cv2.imwrite("../left_tmp/left_tmp.jpg", frame0)
            cv2.imwrite("../right_tmp/right_tmp.jpg", frame1)
            print("capture successed!")
        self.left_frame.clear()
        self.right_frame.clear()
        self.load_img()

    def continue_capture_calculate(self):
        while(1):
            self.auto_get_1_frame()
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



