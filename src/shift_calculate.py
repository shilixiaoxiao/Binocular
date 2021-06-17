# -*- coding: utf-8 -*-
"""

Created on 2021/6/10
@author: Jimmy
"""
import os
import numpy as np
import cv2
import glob
from stereo_calibration import calibration

class calculate:
    def __init__(self):
        self.cap0 = cv2.VideoCapture(0)
        self.cap1 = cv2.VideoCapture(1)
        self.size = (12,8)

    def capture_1_frame(self):
        cap0 = self.cap0
        cap1 = self.cap1
        while (1):

            ret0, frame0 = cap0.read()
            ret1, frame1 = cap1.read()
            cv2.imshow("capture0", frame0)
            cv2.imshow("capture1", frame1)

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
        cv2.destroyAllWindows()

    def auto_get_1_frame(self):


        ret0, frame0 = self.cap0.read()
        ret1, frame1 = self.cap1.read()
        cv2.imshow("capture0", frame0)
        cv2.imshow("capture1", frame1)

        if ret0 == True and ret1 == True:
            if not os.path.exists("../left_tmp"):
                os.mkdir("../left_tmp")
            if not os.path.exists("../right_tmp"):
                os.mkdir("../right_tmp")
            cv2.imwrite("../left_tmp/left_tmp.jpg", frame0)
            cv2.imwrite("../right_tmp/right_tmp.jpg", frame1)
            print("capture successed!")

    def remap(self):
        #cali = calibration()
        #map1_l,map2_l,map1_r,map2_r = cali.binocular_calibration()
        # undistort the original image, take img#3 as an example
        calibration_file = np.load("parameters for calibration.npz")
        rectification_file = np.load("parameters for rectification.npz")
        mtx_l = calibration_file["mtx_l"]
        print(type(mtx_l))

        mtx_r = calibration_file["mtx_r"]
        print(type(mtx_r))
        dist_l = calibration_file["dist_l"]
        print(type(dist_l))
        dist_r = calibration_file["dist_r"]
        print("dist_r",dist_r)
        R1 = rectification_file["R1"]
        print("R1 = ", R1)
        print(type(R1))
        R2 = rectification_file["R2"]
        print("R2 = ", R2)
        P1 = rectification_file["P1"]
        print("P1 = ",P1)
        print(type(P1))
        P2 = rectification_file["P2"]
        print("P2 = ",P2)
        gray_shape = calibration_file["gray_shape"]
        print("Gray_shape = ",gray_shape)

        #[tuple(x) for x in gray_shape.tolist()]
        #image shape should change when camera resolution changed!
        shape = (640,480)
        #print(type(gray_shape))
        map1_l, map2_l = cv2.initUndistortRectifyMap(mtx_l, dist_l, R1, P1, shape, cv2.CV_16SC2)
        map1_r, map2_r = cv2.initUndistortRectifyMap(mtx_r, dist_r, R2, P2, shape, cv2.CV_16SC2)

        left3, right3 = self.get_tmp_img()
        #left3 = cv2.imread('../left_tmp/left_tmp.jpg')
        left_gray = cv2.cvtColor(left3,cv2.COLOR_BGR2GRAY)
        #dst_l = cv2.remap(left3, map1_l, map2_l, cv2.INTER_LINEAR)
        dst_l = cv2.remap(left_gray, map1_l, map2_l, 0)
        #cv2.imwrite('rectifyresult/left03(rectified).jpg', dst_l)
        #if cv2.imwrite('rectifyresult/left03(rectified).jpg', dst_l) == True:
        #    print('rectification of left camera has been done successfully.\n')
        #right3 = cv2.imread('../right_tmp/right_tmp.jpg')
        right_gray = cv2.cvtColor(right3, cv2.COLOR_BGR2GRAY)
        #dst_r = cv2.remap(right3, map1_r, map2_r, cv2.INTER_LINEAR)
        dst_r = cv2.remap(right_gray, map1_r, map2_r, 0)
        # cv2.imwrite('rectifyresult/right03(rectified).jpg', dst_r)
        # if cv2.imwrite('rectifyresult/right03(rectified).jpg', dst_r) == True:
        #     print('rectification of right camera has been done successfully.\n')

        corners_l = []
        corners_r = []

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        #gray_l = cv2.cvtColor(dst_l, cv2.COLOR_BGR2GRAY)
        #gray_r = cv2.cvtColor(dst_r, cv2.COLOR_BGR2GRAY)

        cv2.imshow("dst_l", dst_l)
        cv2.imshow("dst_r", dst_r)
        cv2.waitKey(1000)
        imgpoints1 = []
        imgpoints2 = []
        # cv2.CALIB_CB_ADAPTIVE_THRESH

        # ret, corners = cv2.findChessboardCorners(gray, (15, 11), None)
        ret1, corners_left = cv2.findChessboardCorners(dst_l, self.size, None)

        if ret1 == True:
            corners_l = cv2.cornerSubPix(dst_l, corners_left, (11, 11), (-1, -1), criteria)
            imgpoints1.append(corners_l)

        ret2, corners_right = cv2.findChessboardCorners(dst_r, self.size, None)

        if ret2 == True:
            corners_r = cv2.cornerSubPix(dst_r, corners_right, (11, 11), (-1, -1), criteria)
            imgpoints2.append(corners_r)

        if ret1 == True and ret2 == True:

            # print(corners_l)
            # print(corners_r)
            shift = corners_l[82] - corners_r[82]
            # shift_x = corners_l[82][0] - corners_l[82][0]
            # shift_y = corners_r[82][1] - corners_r[82][1]
            # print(shift_x,shift_y)
            print(shift)
        else:
            print("corner found failed!")

    def get_tmp_img(self):
        img1 = cv2.imread("../left_tmp/left_tmp.jpg")
        img2 = cv2.imread("../right_tmp/right_tmp.jpg")
        return img1,img2

    #def draw_corner(self,img):

    def shift_calc(self):

        corners_l = []
        corners_r = []
        dst_l,dst_r = self.get_tmp_img()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        gray_l = cv2.cvtColor(dst_l, cv2.COLOR_BGR2GRAY)
        gray_r = cv2.cvtColor(dst_r, cv2.COLOR_BGR2GRAY)

        cv2.imshow("dst_l",gray_l)
        cv2.imshow("dst_r",gray_r)
        cv2.waitKey(2000)
        imgpoints1 = []
        imgpoints2 = []
        #cv2.CALIB_CB_ADAPTIVE_THRESH

        #ret, corners = cv2.findChessboardCorners(gray, (15, 11), None)
        ret1, corners_left = cv2.findChessboardCorners(gray_l, self.size, None)

        if ret1 == True:
            corners_l = cv2.cornerSubPix(gray_l, corners_left, (11, 11), (-1, -1), criteria)
            imgpoints1.append(corners_l)

        ret2, corners_right = cv2.findChessboardCorners(gray_r, self.size, None)

        if ret2 == True:
            corners_r = cv2.cornerSubPix(gray_r, corners_right, (11, 11), (-1, -1), criteria)
            imgpoints2.append(corners_r)

        if ret1 == True and ret2 == True:

            #print(corners_l)
            #print(corners_r)
            shift = corners_l[48] - corners_r[48]
            #shift = corners_l[82] - corners_r[82]
            # shift_x = corners_l[82][0] - corners_l[82][0]
            # shift_y = corners_r[82][1] - corners_r[82][1]
            # print(shift_x,shift_y)
            print(shift)
        else:
            print("corner found failed!")


