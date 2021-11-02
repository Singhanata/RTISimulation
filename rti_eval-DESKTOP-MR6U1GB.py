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

def calDerivative(iM,**kw):
    axis = 'x'
    if 'axis' in kw:
        axis = kw['axis']
    direct = 'f'
    if 'direction' in kw:
        direct = kw['direction']
    
    kerneL = np.zeros((3,3))
    if direct == 'f':
        kerneL[1] = -1
        kerneL[2] = 1
    elif direct == 'c':
        kerneL[0] = -1
        kerneL[2] = 1
    elif direct == 'b':
        kerneL[0] = -1
        kerneL[1] = 1
    else:
        raise ValueError('direction of derivative is not defined')
        
    if axis == 'x':
        pass
    if axis == 'y':
        kerneL = kerneL.T
    
    return convolve(iM, kernel)

def convolve()
        
    