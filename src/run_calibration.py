# -*- coding: utf-8 -*-
"""

Created on 2021/6/10
@author: Jimmy
"""

import numpy as np
import cv2
import glob

from stereo_calibration import calibration
from shift_calculate import calculate


calc = calculate()
cali = calibration()

#cali.capture_calibration()
#cali.binocular_calibration()
#calc.capture_1_frame()
#calc.remap()

while(1):
    calc.auto_get_1_frame()

    calc.get_tmp_img()
    calc.shift_calc()





