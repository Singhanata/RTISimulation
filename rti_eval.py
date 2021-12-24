# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 14:54:08 2021

@author: krong
"""
import numpy as np
import math

from rti_rec import RecordIndex, result_record, conclude_record
from rti_plot import plotRTIIm, plotDerivative, process_boxplot

class RTIEvaluation:
    def __init__(self, paramset, paramlabel, resultset, **kw):
        self.paramset = paramset
        self.paramlabel = paramlabel
        self.resultset = resultset
        self.gfx_enabled = False
        self.rec_enabled = False
        if 'gfx_enabled' in kw:
            self.gfx_enabled = kw['gfx_enabled']
        if 'rec_enabled' in kw:
            self.rec_enabled = kw['record_enabled']
        self.data = {}
        datadim = []
        if 'param1' in kw:
            self.param1 = kw['param1']
            datadim.append(len(kw['param1']))
        if 'param2' in kw:
            self.param2 = kw['param2']
            datadim.append(len(kw['param2']))
        if 'param3' in kw:
            self.param3 = kw['param3']
            datadim.append(len(kw['param3']))
        else:
            if 'sample_size' in kw and kw['sample_size'] > 1:
                self.sample_size = kw['sample_size'] 
                datadim.append(kw['sample_size']) 
        for l in resultset:    
            self.data[l] = np.zeros(datadim)
            
    def evaluate(self, sim, l_a, reF, imagE, idx, key, savepath):
        r = RMSEEvaluation(reF, imagE)
        r.update(derivativeEval(reF, imagE))
        for i, e in enumerate(self.resultset):
            self.data[e][idx[0]][idx[1]][idx[2]] = r[e.name]
        
        if self.rec_enabled: result_record(savepath['rec'], 
                                    key, 
                                    x = sim.coorD(axis=0),
                                    y = sim.coorD(axis=1),
                                    ref = reF,
                                    image = imagE,
                                    results = r)
        if self.gfx_enabled:
            plotRTIIm(sim.scheme,
                    imagE, 
                    path = savepath['gfx'],
                    filename = sim.getTitle('', True) + '_' + key,
                    title = sim.getTitle(), 
                    label = 'Rel. Attenuation',  
                    rmse = r['rmse_all'])
            plotDerivative(sim.scheme,
                    r,
                    path = savepath['gfx'],
                    filename = sim.getTitle('', True) + '_' + key,
                    title = sim.getTitle(),
                    label = 'Derivative of Attenuation',
                    caption = 'border@' 
                    + '{:.3f}'.format(r['border'])
                    + ', '
                    + 'non-border@' 
                    + '{:.3f}'.format(r['non-border']))
        return r

    def conclude(self, savepath, setting):
        # record results
        conclude_record(savepath, setting, self)
        # show gfx
        for e in self.resultset:
            yLabel = e.name
            ptitle = ('a@' + str(setting['area_dimension']) +  
                     'v@' + str(setting['voxel_dimension']) + 
                     'o@' + str(setting['object_dimension']) + 
                     'n@' + str(setting['n_sensor']) + '-' +
                     setting['schemeType'] +
                     setting['weightalgorithm'] + '-')
            p = self.paramset[0]
            xlabel = self.paramlabel[1]
            tl = ptitle + p + '@'
            for i, v in enumerate(self.param1):
                tlv = tl + str(v)
                process_boxplot(self.data[e][i].T, 
                                title = tlv,
                                xlabel = xlabel,
                                ylabel = yLabel,
                                ticklabel = self.param2,
                                path = savepath,
                                filename = e.name + '-' + tlv)
        
        for e in self.resultset:
            yLabel = e.name
            ptitle = ('a@' + str(setting['area_dimension']) +  
                     'v@' + str(setting['voxel_dimension']) + 
                     'o@' + str(setting['object_dimension']) + 
                     'n@' + str(setting['n_sensor']) + '-' +
                     setting['schemeType'] +
                     setting['weightalgorithm'] + '-')
            p = self.paramset[1]
            tl = ptitle + p + '@'
            xlabel = self.paramlabel[0]
            for i, v in enumerate(self.param2):
                tlv = tl + str(v)
                data = []
                for j in range(len(self.param1)):
                    data.append(self.data[e][j][i])
                process_boxplot(data, 
                                title = tlv,
                                xlabel = xlabel,
                                ylabel = yLabel,
                                ticklabel = self.param1,
                                path = savepath,
                                filename = e.name + '-' + tlv)
        
                
                
def RMSEEvaluation(reF, reS):
    results = {}
    idx_obJ = (reF==1)
    idx_noN = (reF==0)

    results[RecordIndex.OBJ_MEAN.name] = reS[idx_obJ].mean()
    results[RecordIndex.NON_MEAN.name] = reS[idx_noN].mean()
    results[RecordIndex.RMSE_ALL.name] = math.sqrt(
                                            np.square(np.subtract(reF, 
                                                          reS)).mean())
    results[RecordIndex.RMSE_OBJ.name] = math.sqrt(
                                            np.square(np.subtract(reF[idx_obJ],
                                                          reS[idx_obJ]))
                                                            .mean())
    results[RecordIndex.RMSE_NON.name] = math.sqrt(
                                            np.square(np.subtract(reF[idx_noN],
                                                      reS[idx_noN]))
                                                        .mean())
    return results

def derivativeEval(reF, reS):
    results = {}

    idx_obJ = (reF==1)
    idx_bordeR = _getBorderIdx(idx_obJ)
    idx_nonBordeR = (~idx_bordeR)
    idx_noN = (reF==0)

    results[RecordIndex.DERIVATIVE_X.name] = calDerivative(reS, 
                                                           axis='x', 
                                                           direction = 'f')

    results[RecordIndex.DERIVATIVE_Y.name] = calDerivative(reS, 
                                                           axis='y', 
                                                           direction = 'f')

    results[RecordIndex.DERIVATIVE_ABS.name] = np.sqrt(results[RecordIndex
                                                                 .DERIVATIVE_X
                                                                 .name]**2 
                                                       + results[RecordIndex
                                                                 .DERIVATIVE_Y
                                                                 .name]**2)

    results[RecordIndex.DERIVATIVE_MEAN.name] = results[RecordIndex
                                                        .DERIVATIVE_ABS
                                                        .name].mean()

    results[RecordIndex.DERIVATIVE_OBJ.name] = (results[RecordIndex
                                                        .DERIVATIVE_ABS
                                                        .name]
                                                        [idx_obJ]
                                                        .mean())
    results[RecordIndex.DERIVATIVE_NON.name] = (results[RecordIndex
                                                        .DERIVATIVE_ABS
                                                        .name]
                                                        [idx_noN]
                                                        .mean())
    results[RecordIndex.DERIVATIVE_BORDER.name] = (results[RecordIndex
                                                           .DERIVATIVE_ABS
                                                           .name]
                                                           [idx_bordeR]
                                                           .mean())
    results[RecordIndex.DERIVATIVE_NONBORDER.name] = (results[RecordIndex
                                                           .DERIVATIVE_ABS
                                                           .name]
                                                           [idx_nonBordeR]
                                                           .mean())
    results[RecordIndex.DERIVATIVE_BORDERRATIO.name] = (results[RecordIndex
                                                           .DERIVATIVE_BORDER
                                                           .name]
                                                    /results[RecordIndex
                                                            .DERIVATIVE_MEAN
                                                            .name])
    results[RecordIndex.DERIVATIVE_NONBORDERRATIO.name] = (results[RecordIndex
                                                        .DERIVATIVE_NONBORDER
                                                        .name]
                                                    /results[RecordIndex
                                                            .DERIVATIVE_MEAN
                                                            .name])
    
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

def _getBorderIdx(idx_obJ):
    
    bU = np.roll(idx_obJ, -1, axis=0)
    bU = (bU!=idx_obJ)
    bD = np.roll(idx_obJ, 1, axis=0)
    bD = (bD!=idx_obJ)
    bL = np.roll(idx_obJ, -1, axis=1)
    bL = (bU!=idx_obJ)
    bR = np.roll(idx_obJ, 1, axis=1)
    bR = (bU!=idx_obJ)
    
    bUL = np.roll(bU, -1, axis=1)
    bUR = np.roll(bU, 1, axis=1)
    bDL = np.roll(bD, -1, axis=1)
    bDR = np.roll(bD, 1, axis=1)

    bLU = np.roll(bL, -1, axis=0)
    bLD = np.roll(bU, 1, axis=0)
    bRU = np.roll(bD, -1, axis=0)
    bRD = np.roll(bD, 1, axis=0)
    
    return (bU|bD|bL|bR|bUL|bUR|bDL|bDR|bLU|bLD|bRU|bRD)


