# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 09:11:05 2021

@author: krong
"""
import numpy as np
from rti_grid import RTIGrid

def reference_object_position(coorD, form, obj_dim = (1., 1.)):
    coordX = coorD[0]
    coordY = coorD[1]
    
    dx = coordX[-1] - coordX[0]
    dy = coordY[-1] - coordY[0]
    obj_pos = []
    
    for f in form:
        op = [0.,0.]
        if f[0] == 'l':
            op[0] = coordX[0]
        elif f[0] == 'c':
            op[0] = coordX[0] + dx/2 - obj_dim[0]/2
        elif f[0] == 'r':
            op[0] = coordX[-1] - obj_dim[0]
        else:
            raise ValueError('form not defined')
        if f[1] == 't':
            op[1] = coordY[-1] - obj_dim[1]
        elif f[1] == 'c':
            op[1] = coordY[0] + dy/2 - obj_dim[1]/2
        elif f[1] == 'b':
            op[1] = coordY[0]
        else:
            raise ValueError('form not defined')
        obj_pos.append(op)
        return obj_pos  
    return 
def simulateInput(scheme, cal, obj_dim=(1.,1.), obj_pos = (0., 0.), **kw):
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
    if 'form' in kw:
        kw['key'] = kw['form']
    else:
        kw['key'] = 'o(' + str(obj_pos[0]) + ',' + str(obj_pos[1]) + ')'
    
    x_range = (obj_pos[0], obj_pos[0] + obj_dim[0])
    y_range = (obj_pos[1], obj_pos[1] + obj_dim[1])
        
    vxS = scheme.getVoxelScenario(x_range, y_range)
    return _calLinkAtten(cal, vxS,  **kw)

def _calLinkAtten(cal, vxS, **kw):
    try:
        vxArr = RTIGrid.reshapeVoxelM2Arr(vxS)
        l_ideal = cal.calIdealLinkAtten(vxArr)
    except ValueError:
        raise ValueError('Dimension mismatch.')
    refInput = {}
    if 'snr_db' in kw:
        kw['snr'] = 10**(kw['snr-db']/10)
    if 'snr' in kw:
        if 'sample_size' in kw:
            for i in range(kw['sample_size']):
                l_snr = __calCorruptedLinkAtten(l_ideal, kw['snr'], mode = kw['mode'])
                key = (kw['key'] + '_snr' 
                                 + '_' 
                                 + str(kw['snr']) + '_' + str(i+1))
                refInput[key] = [l_snr, vxS, i]
            return refInput
        l_snr = __calCorruptedLinkAtten(l_ideal, kw['snr'], mode = kw['mode'])
        key = kw['key'] + '_snr' + str(kw['snr'])
        refInput[key] = [l_snr, vxS, i]
        return refInput
    if 'snr_db_list' in kw:
            for v in kw['snr_db_list']:
                kw['snr_list'].append(10**(kw['snr-db']/10))
    if 'snr_list' in kw:
        for i, v in enumerate(kw['snr_list']):
                l_snr = __calCorruptedLinkAtten(l_ideal, v, mode = kw['mode'])
                key = kw['key'] + '_snr' + '_' + str(v)
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
        mode (integer) : How to calculate the SNR
            0 : calculate based on E[l]
            1 : calculate on each element of l
            other : two-part gaussian mixture model
    Returns
    -------
    Link Attenuation with additive noise

    """
    if not 'mode' in kw or not kw['mode']:
        # sigma is calculated from E[l]
        mu = l.mean()
        sigma = mu/snr
        noise = np.random.normal(0, sigma, l.size)
        ln = l + noise
        
        return ln
    elif kw['mode'] == 1:
        ln = np.zeros(l.size)
        # sigma is calculated for each l element
        for i,val in enumerate(l):
            sigma = val/snr
            noise = np.random.normal() * sigma
            ln[i] = val + noise
        
        return ln
    elif kw['mode'] == 2:
        ln = np.zeros(l.size)
        il = (l!=0)
        mu = l[il].mean()
        sigma = mu/snr
        noise = np.random.normal(0, sigma, l.size)
        ln = l + noise
        
        return ln
    else:
        # call mixlognarmalfading 
        raise ValueError('Mode not implemented')
                    
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