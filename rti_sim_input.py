# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 09:11:05 2021

@author: krong
"""
import numpy as np
from rti_grid import RTIGrid

import math

def reference_object_position(coorD, form, obj_dim = (1., 1.)):
    coordX = coorD[0]
    coordY = coorD[1]
    
    dx = coordX[-1] - coordX[0]
    dy = coordY[-1] - coordY[0]
    obj_pos = []
    
    for f in form:
        op = [0.,0.]
        if f[0] == 'l':
            op[0] = coordX[0] + obj_dim[0]/2
        elif f[0] == 'c':
            op[0] = coordX[0] + dx/2 
        elif f[0] == 'r':
            op[0] = coordX[-1] - obj_dim[0]/2
        else:
            raise ValueError('form not defined')
        if f[1] == 't':
            op[1] = coordY[-1] - obj_dim[1]/2
        elif f[1] == 'c':
            op[1] = coordY[0] + dy/2 
        elif f[1] == 'b':
            op[1] = coordY[0] + obj_dim[1]/2
        else:
            raise ValueError('form not defined')
        obj_pos.append(op)
    return obj_pos 
 
def simulateInput(scheme, cal, obj_pos = (0., 0.), **kw):
    """
    Calculate the reference input based on the simulation conditions and object
    information in 2D

    Parameters
    ----------
    scheme : RTIScheme
        Instance of RTIScheme: all information about setting
    calculator : RTICalculator
        Instance of RTICalculator: Weighting algorithm
    obj_pos : Position
        Position of the left-bottom corner
        obj_pos.x = x-coordination
        obj_pos.y = y-coordination
    obj_dim : Integer List
        (x-dimension length, y-dimension length)
        The default is (1.,1.).

    Keyword Arguments:
        snr (float) : Ratio between signal (mean) and noise (sigma)
        snr-db (float) : snr in [dB]
    Returns
    -------
    refInput : dictionary
        reference input in form of pixel matrix

    """
    obj_dim = (1.,1.)
    if 'object_dimension' in kw:
        obj_dim = kw['object_dimension']
    
    if 'form' in kw:
        kw['key'] = kw['form']
    else:
        kw['key'] = 'o(' + "%.2f"%obj_pos[0] + ',' + "%.2f"%obj_pos[1] + ')'
    if 'object_type' in kw:
        kw['object_form'] = 'cylindical'
    
    x_range = (obj_pos[0] - obj_dim[0]/2, obj_pos[0] + obj_dim[0]/2)
    y_range = (obj_pos[1] - obj_dim[1]/2, obj_pos[1] + obj_dim[1]/2)
        
    vxS = scheme.getVoxelScenario(x_range, y_range, **kw)
    return _calLinkAtten(cal, vxS,  **kw)

def _calLinkAtten(cal, vxS, **kw):
    try:
        vxArr = RTIGrid.reshapeVoxelM2Arr(vxS)
        l_ideal = cal.calIdealLinkAtten(vxArr)
    except ValueError:
        raise ValueError('Dimension mismatch.')
    refInput = {}
    if 'SNR_dB' in kw:
        kw['snr'] = 10**(kw['snr-db']/10)
    if 'SNR' in kw:
        if 'sample_size' in kw:
            for i in range(kw['sample_size']):
                l_snr = __calCorruptedLinkAtten(l_ideal, kw['SNR'], SNR_mode = kw['SNR_mode'])
                key = (kw['key'] + '_SNR' 
                                 + '_' 
                                 + str(kw['SNR']) + '_' + str(i+1))
                refInput[key] = [l_snr, vxS, i]
            return refInput
        l_snr = __calCorruptedLinkAtten(l_ideal, kw['SNR'], SNR_mode = kw['SNR_mode'])
        key = kw['key'] + '_SNR' + str(kw['SNR'])
        refInput[key] = [l_snr, vxS]
        return refInput
    if 'SNR_dB_list' in kw:
            for v in kw['SNR_dB_list']:
                kw['SNR_list'].append(10**(v/10))
    if 'SNR_list' in kw:
        for i, v in enumerate(kw['SNR_list']):
                l_snr = __calCorruptedLinkAtten(l_ideal, v, SNR_mode = kw['SNR_mode'])
                key = kw['key'] + '_SNR' + '_' + str(v)
                refInput[key] = [l_snr, vxS, i]
        return refInput
   
    refInput[kw['key']] = [l_ideal, vxS, 0]        
    return refInput    
               
def __calCorruptedLinkAtten(l, snr, **kw):
    """
    Calculate noise signal according to the SNR and noise model

    Parameters
    ----------
    l : Link Attenuation [dB]
        Array of Link Attenuation 
    SNR : float (% not in [dB])
        Ratio of signal mean and noise sigma [%]
    
    Keyword Args:
        SNR_mode (integer) : How to calculate the SNR
            0 : calculate based on E[l]
            1 : calculate on each element of l
            other : two-part gaussian mixture model
    Returns
    -------
    Link Attenuation with additive noise

    """
    if not 'SNR_mode' in kw or not kw['SNR_mode']:
        # sigma is calculated from E[l]
        mu = l.mean()
        sigma = mu/snr
        noise = np.random.normal(0, sigma, l.size)
        ln = l + noise
        
        return ln
    elif kw['SNR_mode'] == 1:
        ln = np.zeros(l.size)
        # sigma is calculated for each l element
        for i,val in enumerate(l):
            sigma = val/snr
            noise = np.random.normal() * sigma
            ln[i] = val + noise
        
        return ln
    elif kw['SNR_mode'] == 2:
        ln = np.zeros(l.size)
        il = (l!=0)
        mu = abs(l[il].mean())
        sigma = mu/snr
        noise = np.random.normal(0, sigma, l.size)
        ln = l + noise
        
        return ln
    else:
        # call mixlognarmalfading 
        raise ValueError('SNR_mode not implemented')
                    
def mixLognormalfading(p, sigma1):
    """
    This function models Fading in RTI using two-part gaussian mixture model.
    The fading effects in RTI can be modelled by two-part mixture of log-normal
    distribution, i.e., The logarithm of the random variable is a random 
    variable with the gaussian distribution. 

    Parameters
    ----------
    p : float
        Probability of the dominant normal distribution
    sigma1 : float
        Standard deviation of dominant normal distribution

    Returns
    -------
    None.

    """
    # calculate p2 and sigma2 
    # get a sample of uniform [0,1) 
    pass

def sim_trajectory(st, traject):
    tjY = []
    nowP = st
    for tj in traject:
        v = tj[0]
        fr = tj[1]
        dt = 1/fr
        ds = v*dt
        if tj[2] == 'lin':
            for p in tj[3]:
                delx = p[0] - nowP[0]
                dely = p[1] - nowP[1]
                abss = math.sqrt(delx**2 + dely**2)
                dx = ds * delx/abss
                dy = ds * dely/abss
                
                while abs(p[0] - nowP[0]) > abs(dx):
                    tjY.append(nowP)
                    nowP = ((nowP[0] + dx),(nowP[1] + dy))
    return tjY
        