# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 14:54:08 2021

@author: krong
"""

import numpy as np
import math

def RMSEEvaluation(reF, reS):
    return math.sqrt(np.square(np.subtract(reF, reS)).mean())