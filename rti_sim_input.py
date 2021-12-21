# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 09:11:05 2021

@author: krong
"""
import numpy as np
from rti_grid import RTIGrid

def simulateInput(scheme, cal, obj_dim=(1.,1.), **kw):
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
    
    coordX = scheme.selection.coordX
    coordY = scheme.selection.coordY

    dx = coordX[-1] - coordX[0]
    dy = coordY[-1] - coordY[0]
    
    refInput = {}
    
    if  'obj_pos' in kw:
        obj_pos = kw['obj_pos']
        x_range = (obj_pos[0], obj_pos[0] + obj_dim[0])
        y_range = (obj_pos[1], obj_pos[1] + obj_dim[1])
        
        vxS = scheme.getVoxelScenario(x_range, y_range)
        l_Atten = _calIdealLinkAtten(cal, vxS)
        if 'snr-db' in kw:
            kw['snr'] = 10**(kw['snr-db']/10)
        if 'snr' in kw:
            l_Atten = _calCorruptedLinkAtten(l_Atten, kw['snr'])
        refInput = {}
        k = 'o(' + str(obj_pos[0]) + ',' + str(obj_pos[1]) + ')'
        refInput[k] = [l_Atten, vxS]
        
        return refInput
    
    elif kw['form'] == 'center':
        center_x = coordX[0] + dx/2
        center_y = coordY[0] + dy/2

        x_range = (center_x - obj_dim[0]/2, center_x + obj_dim[0]/2)
        y_range = (center_y - obj_dim[1]/2, center_y + obj_dim[1]/2)

        vxS = scheme.getVoxelScenario(x_range, y_range)
        l_Atten = _calIdealLinkAtten(cal, vxS)
        kw['key'] = 'center'
        refInput = _calSNRLinkAtten(l_Atten, vxS, **kw)
            
        return refInput
    
    elif kw['form'] == '9-point':
        x_range_l = (coordX[0], coordX[0] + dx/10)
        x_range_c = (coordX[0] + 4.5*dx/10, coordX[0] + 5.5*dx/10)
        x_range_r = (coordX[0] + 9*dx/10, coordX[0] + 10*dx/10)
    
        y_range_b = (coordY[0], coordY[0] + dy/10)
        y_range_c = (coordY[0] + 4.5*dy/10, coordY[0] + 5.5*dy/10)
        y_range_t = (coordY[0] + 9*dy/10, coordY[0] + 10*dy/10)
    
        vxS_lb = scheme.getVoxelScenario(x_range_l, y_range_b)
        vxS_cb = scheme.getVoxelScenario(x_range_c, y_range_b)
        vxS_rb = scheme.getVoxelScenario(x_range_r, y_range_b)
        vxS_lc = scheme.getVoxelScenario(x_range_l, y_range_c)
        vxS_cc = scheme.getVoxelScenario(x_range_c, y_range_c)
        vxS_rc = scheme.getVoxelScenario(x_range_r, y_range_c)
        vxS_lt = scheme.getVoxelScenario(x_range_l, y_range_t)
        vxS_ct = scheme.getVoxelScenario(x_range_c, y_range_t)
        vxS_rt = scheme.getVoxelScenario(x_range_r, y_range_t)
    
        l_lb = _calIdealLinkAtten(cal, vxS_lb)
        l_cb = _calIdealLinkAtten(cal, vxS_cb)
        l_rb = _calIdealLinkAtten(cal, vxS_rb)
        l_lc = _calIdealLinkAtten(cal, vxS_lc)
        l_cc = _calIdealLinkAtten(cal, vxS_cc)
        l_rc = _calIdealLinkAtten(cal, vxS_rc)
        l_lt = _calIdealLinkAtten(cal, vxS_lt)
        l_ct = _calIdealLinkAtten(cal, vxS_ct)
        l_rt = _calIdealLinkAtten(cal, vxS_rt)
        if 'snr-db' in kw:
            kw['snr'] = 10**(kw['snr-db']/10)
        if 'snr' in kw:
            l_lb = _calCorruptedLinkAtten(l_lb, kw['snr'])
            l_cb = _calCorruptedLinkAtten(l_cb, kw['snr'])
            l_rb = _calCorruptedLinkAtten(l_rb, kw['snr'])
            l_lc = _calCorruptedLinkAtten(l_lc, kw['snr'])
            l_cc = _calCorruptedLinkAtten(l_cc, kw['snr'])
            l_rc = _calCorruptedLinkAtten(l_rc, kw['snr'])
            l_lt = _calCorruptedLinkAtten(l_lt, kw['snr'])
            l_ct = _calCorruptedLinkAtten(l_ct, kw['snr'])
            l_rt = _calCorruptedLinkAtten(l_rt, kw['snr'])
    
        refInput = {}
        refInput['lb'] = [l_lb, vxS_lb]
        refInput['cb'] = [l_cb, vxS_cb]
        refInput['rb'] = [l_rb, vxS_rb]
        refInput['lc'] = [l_lc, vxS_lc]
        refInput['cc'] = [l_cc, vxS_cc]
        refInput['rc'] = [l_rc, vxS_rc]
        refInput['lt'] = [l_lt, vxS_lt]
        refInput['ct'] = [l_ct, vxS_ct]
        refInput['rt'] = [l_rt, vxS_rt]
    
        return refInput

def _calSNRLinkAtten(l_ideal, vxS, **kw):
    refInput = {}
    if 'snr_db' in kw:
        kw['snr'] = 10**(kw['snr-db']/10)
    if 'snr' in kw:
        l_snr = _calCorruptedLinkAtten(l_ideal, kw['snr'])
        key = kw['key'] + '_snr' + str(kw['snr'])
        refInput[key] = [l_snr, vxS]
        if 'sample_size' in kw:
            for i in range(kw['sample_size']):
                l_snr = _calCorruptedLinkAtten(l_ideal, kw['snr'])
                key = (kw['key'] + '_snr' 
                                 + '_' 
                                 + str(kw['snr']) + '_' + str(i+1))
                refInput[key] = [l_snr, vxS]
            return refInput
    if 'snr_db_list' in kw:
            for v in kw['snr_db_list']:
                kw['snr_list'].append(10**(kw['snr-db']/10))
    if 'snr_list' in kw:
        for v in kw['snr_list']:
                l_snr = _calCorruptedLinkAtten(l_ideal, v)
                key = kw['key'] + '_snr' + '_' + str(v)
                refInput[key] = [l_snr, vxS]
        return refInput
   
    refInput[kw['key']] = [l_ideal, vxS]        
    return refInput    
       
def _calIdealLinkAtten(wc, voxelAttenM):
    try:
        vxArr = RTIGrid.reshapeVoxelM2Arr(voxelAttenM)
        linkAttenArr = wc.calIdealLinkAtten(vxArr)
        return linkAttenArr
    except ValueError:
        raise ValueError('Dimension mismatch.')
        
def _calCorruptedLinkAtten(l, snr, **kw):
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
        mu = sum(l)/len(l)
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