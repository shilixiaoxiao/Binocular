# -*- coding: utf-8 -*-


import numpy as np
import cv2
import glob
import sys

img_left = cv2.imread("../left_cali_5/left00.jpg")
img_right = cv2.imread("../right_cali_5/right00.jpg")
gray_left = cv2.cvtColor(img_left,cv2.COLOR_BGR2GRAY)
gray_right = cv2.cvtColor(img_right,cv2.COLOR_BGR2GRAY)
point_left = []
point_right = []
ret_left, corners_left = cv2.findChessboardCorners(gray_left, (12,8), None)
ret_right, corners_right = cv2.findChessboardCorners(gray_right, (12,8), None)
if ret_left == True and ret_right == True:
    point_left.append(corners_left)
    point_right.append(corners_right)
M = cv2.estimateAffine2D(point_left,point_right,maxIters=100,ransacReprojThreshold=20)
print(M)
# edges_left = cv2.Canny(gray_left,50,150,apertureSize=3)
# edges_right = cv2.Canny(gray_right,50,150,apertureSize=3)
#
# lines_left = cv2.HoughLines(edges_left,1,np.pi/1800,118)
# lines_right = cv2.HoughLines(edges_right,1,np.pi/1800,118)
#
# for line in lines_left:
#     rho = line[0][0]
#     theta = line[0][1]
#     if rho > 200:
#         print(rho)
#         print(theta)
# for line in lines_right:
#     rho = line[0][0]
#     theta = line[0][1]
#     if rho > 200:
#         print(rho)
#         print(theta)
# cv2.imshow("canny_left",edges_left)
# cv2.imshow("canny_right",edges_right)
# cv2.waitKey(0)
# cv2.destroyAllWindows()