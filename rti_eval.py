# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 14:54:08 2021

@author: krong
"""

import numpy as np
import math

def RMSEEvaluation(reF, reS, **kw):
    results = {}
    idx_obJ = (reF==1)
    idx_noN = (reF==0)
    
    question = ''
    if 'question' in kw:
        question = kw['question']
    
    if not question:
        results['rmse_all'] = math.sqrt(np.square(np.subtract(reF, 
                                                              reS)).mean())
      
        results['obj_mean'] = reS[idx_obJ].mean()
        results['non_mean'] = reS[idx_noN].mean()
        results['rmse_obj'] = math.sqrt(np.square(np.subtract(reF[idx_obJ],
                                                              reS[idx_obJ]))
                                                                .mean())
        results['rmse_non'] = math.sqrt(np.square(np.subtract(reF[idx_noN],
                                                          reS[idx_noN]))
                                                            .mean())
    elif question == 'all':
        results['rmse_all'] = math.sqrt(np.square(np.subtract(reF, 
                                                              reS)).mean())
    elif question == 'non':
        results['non_mean'] = reS[idx_noN].mean()
        results['rmse_non'] = math.sqrt(np.square(np.subtract(reF[idx_noN],
                                                          reS[idx_noN]))
                                                            .mean())
    elif question == 'obj':
        results['obj_mean'] = reS[idx_obJ].mean()
        results['rmse_obj'] = math.sqrt(np.square(np.subtract(reF[idx_obJ],
                                                              reS[idx_obJ]))
                                                                .mean())
    else:
        raise ValueError('question is not defined')
        
    return results

def derivativeEval(reF, reS, **kw):
    results = {}

    idx_obJ = (reF==1)
    idx_noN = (reF==0)

    question = ''
    if 'question' in kw:
        question = kw['question'] 

    if not question:
        results['x'] = calDerivative(reS, axis='x', direction = 'f')
        results['y'] = calDerivative(reS, axis='y', direction = 'f')
        results['abs'] = np.sqrt(results['x']**2 + results['y']**2)
        results['obj-derivative'] = results['abs'][idx_obJ].mean()
        results['non-derivative'] = results['abs'][idx_noN].mean()        
    elif question == 'x':
        results['x'] = calDerivative(reS, axis='x', direction = 'f')
    elif question == 'y':
        results['y'] = calDerivative(reS, axis='y', direction = 'f')
    else:
        raise ValueError('question is not defined')
    
    if 'indexOfInterest' in kw:
        a_x = kw['indexOfInterest'][0]
        a_y = kw['indexOfInterest'][1]
        results['x_interest'] = results['x'][:,a_x]
        results['y_interest'] = results['y'][a_y,:]
    return results

def calDerivative(iM, **kw):
    axis = 'x'
    if 'axis' in kw:
        axis = kw['axis']
    direct = 'c'
    if 'direction' in kw:
        direct = kw['direction']

    kernel = np.zeros((3,1))
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
        pass
    elif axis == 'y':
        kernel = kernel.T
    else:
        raise ValueError('axis of derivative is not defined')

    return convolve2D(iM, kernel)

def convolve2D(iM, kernel, **kw):
    """
    Calculation of convolution between image and kernel

    Parameters
    ----------
    iM : 2D Numpy Array
        2D image matrix.
    kernel : 2D Numpy Array
        2D Filter.
    **kw : Keyword Arguments
        paddingDirection = {'c'|'b'|'f'}

    Raises
    ------
    ValueError
        Keyword Padding direction can only be {'c', 'f', 'b'}.
        Padding direction 'c' requires kernel size in odd number, i.e.,
        (3x3, 5x5, ...)
    Returns
    -------
    output : 2D Numpy Array
        DESCRIPTION.

    """
    padDir = 'c'
    if 'paddingDirection' in kw:
        padDir = kw['paddingDirection']
    
    k_x = kernel.shape[0]
    k_y = kernel.shape[1]

    iM_x = iM.shape[0]
    iM_y = iM.shape[1]

    padSize_x = k_x-1
    padSize_y = k_y-1
    
    temP = np.zeros((iM_x+padSize_x, iM_y+padSize_y))
    
    if padDir == 'c':
        if (padSize_x%2 or padSize_y%2):
            raise ValueError('Padding is not symmetric')
        padSize_x = int(padSize_x/2)
        padSize_y = int(padSize_y/2)
        
        temP[padSize_x:padSize_x
             +iM_x, padSize_y:padSize_y+iM_y] = iM
        for i in range(padSize_x):
            temP[i] = temP[padSize_x]
            idx = i+1
            temP[-idx] = temP[-(padSize_x+1)]
        for i in range(padSize_y):
            temP[:,i] = temP[:,padSize_y]
            idx = i+1
            temP[:,-1] = temP[:,-(padSize_y+1)]
    elif padDir == 'b':
        temP[padSize_x:iM_x + padSize_x, padSize_y:iM_y + padSize_y] = iM
        for i in range(padSize_x):
            temP[:,i] = temP[:,padSize_x]
        for i in range(padSize_y):    
            temP[i] = temP[padSize_y]
    elif padDir == 'f':
        temP[0:iM_x, 0:iM_y] = iM
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
            output[x,y] = (kernel * temP[x:x+k_x, y:y+k_y]).sum()
            
    return output






