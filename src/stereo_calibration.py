# -*- coding: utf-8 -*-
"""

Created on 2021/6/10
@author: Jimmy
"""

import numpy as np
import cv2
import glob
import os


class calibration():
    # monocular camera calibration
    def __init__(self):
        self.size = (12,8)
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.objp = np.zeros((8 * 12, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:12, 0:8].T.reshape(-1, 2)
        self.objpoints = []
        self.imgpoints1 = []
        self.imgpoints2 = []
        self.cap0 = cv2.VideoCapture(0)
        self.cap1 = cv2.VideoCapture(1)
        self.path_left = "../left_cali_6"
        self.path_right = "../right_cali_6"

    def capture_calibration(self):
        n = 0
        while(1):
            ret0, frame0 = self.cap0.read()
            ret1, frame1 = self.cap1.read()
            #cv2.imshow("capture0",frame0)
            #cv2.imshow("capture1",frame1)


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
        cv2.destroyAllWindows()

    def monocular_calibration(self):

        # left camera calibration
        images = glob.glob(self.path_left + '/*.jpg')
        l = 1
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, self.size, None)
            print("loading:l" + str(l))
            l += 1
            if ret == True:
                self.objpoints.append(self.objp)
                corners2=cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), self.criteria)
                self.imgpoints1.append(corners2)
                print("NO.l" + str(l) + "load successed!")
            else:
                print("NO.l" + str(l) + "load failed")

        ret, mtx_l, dist_l, rvecs_l, tvecs_l = cv2.calibrateCamera(self.objpoints, self.imgpoints1, gray.shape[::-1],None,None)

        # right camera calibration

        images = glob.glob(self.path_right + '/*.jpg')
        r = 1
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, self.size, None)
            print("load:r" + str(r))
            r += 1
            if ret == True:
                corners2=cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), self.criteria)
                self.imgpoints2.append(corners2)
            else:
                print("NO.r" + str(r) + "load failed")
        ret, mtx_r, dist_r, rvecs_r, tvecs_r = cv2.calibrateCamera(self.objpoints, self.imgpoints2, gray.shape[::-1],None,None)
        gray_shape = gray.shape[::-1]

        np.savez("points.npz",objpoints=self.objpoints,imgpoints1=self.imgpoints1,imgpoints2=self.imgpoints2)
        return mtx_l,mtx_r,dist_l,dist_r,gray_shape

    def binocular_calibration(self):
        # binocular camera calibration
        mtx_l,mtx_r,dist_l,dist_r,gray_shape = calibration.monocular_calibration(self)
        ret, mtx_l, dist_l, mtx_r, dist_r, R, T, E, F = cv2.stereoCalibrate(self.objpoints, self.imgpoints1, self.imgpoints2,
                                                                            mtx_l, dist_l, mtx_r, dist_r, gray_shape)

        np.savez("parameters for calibration.npz",ret=ret,mtx_l=mtx_l,mtx_r=mtx_r,dist_l=dist_l,dist_r=dist_r,R=R,T=T,gray_shape=gray_shape)

        print('intrinsic matrix of left camera=\n', mtx_l)
        print('intrinsic matrix of right camera=\n', mtx_r)
        print('distortion coefficients of left camera=\n', dist_l)
        print('distortion coefficients of right camera=\n', dist_r)
        print('Transformation from left camera to right:\n')
        print('R=\n', R)
        print('\n')
        print('T=\n', T)
        print('\n')
        print('Reprojection Error=\n', ret)

        # stereo rectification立体矫正
        R1, R2, P1, P2, Q, ROI1, ROI2= cv2.stereoRectify(mtx_l, dist_l, mtx_r, dist_r, gray_shape, R, T, flags=0, alpha=-1)

        # undistort rectifying mapping
        map1_l, map2_l = cv2.initUndistortRectifyMap(mtx_l, dist_l, R1, P1, gray_shape, cv2.CV_16SC2)
        map1_r, map2_r = cv2.initUndistortRectifyMap(mtx_r, dist_r, R2, P2, gray_shape, cv2.CV_16SC2)
        np.savez("parameters for rectification.npz", R1=R1, R2=R2, P1=P1, P2=P2, Q=Q, ROI1=ROI1, ROI2=ROI2)
        return map1_l,map2_l,map1_r,map2_r

        # undistort the original image, take img#3 as an example
        # left3 = cv2.imread('../left/left03.jpg')
        # dst_l = cv2.remap(left3, map1_l, map2_l, cv2.INTER_LINEAR)
        # cv2.imwrite('rectifyresult/left03(rectified).jpg', dst_l)
        # if cv2.imwrite('rectifyresult/left03(rectified).jpg', dst_l)==True:
        #     print('rectification of left camera has been done successfully.\n')
        # right3 = cv2.imread('../right/right03.jpg')
        # dst_r = cv2.remap(right3, map1_r, map2_r, cv2.INTER_LINEAR)
        # cv2.imwrite('rectifyresult/right03(rectified).jpg', dst_r)
        # if cv2.imwrite('rectifyresult/right03(rectified).jpg', dst_r) == True:
        #     print('rectification of right camera has been done successfully.\n')
        #
        # np.savez("parameters for rectification.npz", R1=R1, R2=R2, P1=P1, P2=P2, Q=Q, ROI1=ROI1, ROI2=ROI2)
