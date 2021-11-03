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
    padDir = 'f'
    if 'paddingDirection' in kw:
        padDir = kw['paddingDirection']
    
    k_x = kernel.shape[0]
    k_y = kernel.shape[1]

    iM_x = iM.shape[0]
    iM_y = iM.shape[1]

    padSize_x = k_x-1
    padSize_y = k_y-1
    
    temP = np.zeros((iM_x+padSize_x, iM_y+padSize_y))

    begin_x = 0
    end_x = 0
    begin_y = 0
    end_y = 0
    
    if padDir == 'c':
        if (padSize_x%2 or padSize_y%2):
            raise ValueError('Padding is not symmetric')
        padSize_x = padSize_x/2
        padSize_y = padSize_y/2
        
        temP[1:1+iM_x, 1:1+iM_y] = iM
        begin_x = 1
        end_x = 1+iM_x
        begin_y = 1
        end_y = 1+iM_y
        for i in range(padSize_x):
            temP[:,i] = temP[:,padSize_x]
            idx = i+1
            temP[:,-idx] = temP[:,-(padSize_x+1)]
        for i in range(padSize_y):
            temP[i] = temP[padSize_y]
            idx = i+1
            temP[-1] = temP[-(padSize_y+1)]
    elif padDir == 'b':
        temP[padSize_x:iM_x + padSize_x, padSize_y:iM_y + padSize_y] = iM
        begin_x = padSize_x
        end_x = padSize_x+iM_x
        begin_y = padSize_y
        end_y = padSize_y+iM_y
        for i in range(padSize_x):
            temP[:,i] = temP[:,padSize_x]
        for i in range(padSize_y):    
            temP[i] = temP[padSize_y]
    elif padDir == 'f':
        temP[0:iM_x, 0:iM_y] = iM
        begin_x = 0
        end_x = iM_x
        begin_y = 0
        end_y = iM_y
        for i in range(padSize_y):
            idx = i+1
            temP[:,-idx] = temP[:,-(padSize_y+1)]
        for i in range(padSize_y):    
            temP[-(i+1)] = temP[-(padSize_y+1)]
    else:
        raise ValueError('Padding direction not defined')
        
    output = np.zeros((iM.shape[0], iM.shape[1]))
    for x in range(iM_x):
        for y in range(iM_y): 
            output[x,y] = (kernel * temP[x:x+k_x, y:y+k_y])
        






