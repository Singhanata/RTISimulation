# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 14:54:08 2021

@author: krong
"""

import numpy as np
import math

def RMSEEvaluation(reF, reS):
    results = {}
    results['rmse_all'] = math.sqrt(np.square(np.subtract(reF, reS)).mean())

    idx_obJ = (reF==1)
    idx_noN = (reF==0)

    results['obj_mean'] = reS[idx_obJ].mean()
    results['non_mean'] = reS[idx_noN].mean()
    results['rmse_obj'] = math.sqrt(np.square(np.subtract(reF[idx_obJ],
                                                          reS[idx_obJ]))
                                                            .mean())
    results['rmse_non'] = math.sqrt(np.square(np.subtract(reF[idx_noN],
                                                          reS[idx_noN]))
                                                            .mean())

    return math.sqrt(np.square(np.subtract(reF, reS)).mean())

def calDerivative(iM, **kw):
    axis = 'x'
    if 'axis' in kw:
        axis = kw['axis']
    direct = 'f'
    if 'direction' in kw:
        direct = kw['direction']

    kernel = np.zeros((3,3))
    if direct == 'f':
        kernel[1] = -1
        kernel[2] = 1
    elif direct == 'c':
        kernel[0] = -1
        kernel[2] = 1
    elif direct == 'b':
        kernel[0] = -1
        kernel[1] = 1
    else:
        raise ValueError('derivative direction is not defined')

    if axis == 'x':
        kernel = kernel.T
    elif axis == 'y':
        pass
    else:
        raise ValueError('axis of derivative is not defined')

    return convolve2D(iM, kernel)

def convolve2D(iM, kernel, **kw):
    padDir = 'c'
    if 'paddingDirection' in kw:
        padDir = kw['paddingDirection']
    
    k_x = kernel.shape[0]
    k_y = kernel.shape[1]

    iM_x = iM.shape[0]
    iM_y = iM.shape[1]

    temP = np.zeros((iM_x+(k_x-1), iM_y+(k_y-1)))
    if padDir == 'c':
    temP[1:1+iM_x, 1:1+iM_y] = iM
    temP[:,0] = temP[:,0]
    temP[:,-1] = temP[:,-2]
    temP[0] = temP[1]
    temP[-1] = temP[-2]







