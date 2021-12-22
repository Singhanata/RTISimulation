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
        
        kw['key'] = 'o(' + str(obj_pos[0]) + ',' + str(obj_pos[1]) + ')'
        vxS = scheme.getVoxelScenario(x_range, y_range)
        refInput = _calLinkAtten(cal, vxS, **kw)
        
        return refInput
    elif kw['form'] == 'lt':
        center_x = coordX[0] 
        center_y = coordY[0] - obj_dim[1]

        x_range = (center_x - obj_dim[0]/2, center_x + obj_dim[0]/2)
        y_range = (center_y - obj_dim[1]/2, center_y + obj_dim[1]/2)

        kw['key'] = 'lt'
        vxS = scheme.getVoxelScenario(x_range, y_range)
        refInput = _calLinkAtten(cal, vxS,  **kw)
            
        return refInput
    elif kw['form'] == 'ct':
        center_x = coordX[0] + dx/2
        center_y = coordY[0] - obj_dim[1]

        x_range = (center_x - obj_dim[0]/2, center_x + obj_dim[0]/2)
        y_range = (center_y - obj_dim[1]/2, center_y + obj_dim[1]/2)

        kw['key'] = 'ct'
        vxS = scheme.getVoxelScenario(x_range, y_range)
        refInput = _calLinkAtten(cal, vxS,  **kw)
            
        return refInput
    elif kw['form'] == 'rt':
        center_x = coordX[-1] - obj_dim[0]
        center_y = coordY[0] - obj_dim[1]

        x_range = (center_x - obj_dim[0]/2, center_x + obj_dim[0]/2)
        y_range = (center_y - obj_dim[1]/2, center_y + obj_dim[1]/2)

        kw['key'] = 'rt'
        vxS = scheme.getVoxelScenario(x_range, y_range)
        refInput = _calLinkAtten(cal, vxS,  **kw)
            
        return refInput    
    elif kw['form'] == 'lc':
        center_x = coordX[0] 
        center_y = coordY[0] + dy/2

        x_range = (center_x - obj_dim[0]/2, center_x + obj_dim[0]/2)
        y_range = (center_y - obj_dim[1]/2, center_y + obj_dim[1]/2)

        kw['key'] = 'lc'
        vxS = scheme.getVoxelScenario(x_range, y_range)
        refInput = _calLinkAtten(cal, vxS,  **kw)
            
        return refInput
    elif kw['form'] == 'cc':
        center_x = coordX[0] + dx/2
        center_y = coordY[0] + dy/2

        x_range = (center_x - obj_dim[0]/2, center_x + obj_dim[0]/2)
        y_range = (center_y - obj_dim[1]/2, center_y + obj_dim[1]/2)

        kw['key'] = 'cc'
        vxS = scheme.getVoxelScenario(x_range, y_range)
        refInput = _calLinkAtten(cal, vxS,  **kw)
        
        return refInput
    elif kw['form'] == 'rc':
        center_x = coordX[-1] - obj_dim[0]
        center_y = coordY[0] + dy/2

        x_range = (center_x - obj_dim[0]/2, center_x + obj_dim[0]/2)
        y_range = (center_y - obj_dim[1]/2, center_y + obj_dim[1]/2)

        kw['key'] = 'rc'
        vxS = scheme.getVoxelScenario(x_range, y_range)
        refInput = _calLinkAtten(cal, vxS,  **kw)
            
        return refInput
    elif kw['form'] == 'lb':
        center_x = coordX[0] 
        center_y = coordY[0] 

        x_range = (center_x - obj_dim[0]/2, center_x + obj_dim[0]/2)
        y_range = (center_y - obj_dim[1]/2, center_y + obj_dim[1]/2)

        kw['key'] = 'lb'
        vxS = scheme.getVoxelScenario(x_range, y_range)
        refInput = _calLinkAtten(cal, vxS,  **kw)
            
        return refInput
    elif kw['form'] == 'cb':
        center_x = coordX[0] + dx/2
        center_y = coordY[0] 

        x_range = (center_x - obj_dim[0]/2, center_x + obj_dim[0]/2)
        y_range = (center_y - obj_dim[1]/2, center_y + obj_dim[1]/2)

        kw['key'] = 'cb'
        vxS = scheme.getVoxelScenario(x_range, y_range)
        refInput = _calLinkAtten(cal, vxS,  **kw)
            
        return refInput
    elif kw['form'] == 'rb':
        center_x = coordX[-1] - obj_dim[0]
        center_y = coordY[0]

        x_range = (center_x - obj_dim[0]/2, center_x + obj_dim[0]/2)
        y_range = (center_y - obj_dim[1]/2, center_y + obj_dim[1]/2)

        kw['key'] = 'rb'
        vxS = scheme.getVoxelScenario(x_range, y_range)
        refInput = _calLinkAtten(cal, vxS,  **kw)
            
        return refInput
    
    elif kw['form'] == 'ref':
        x_range_l = (coordX[0], coordX[0] + dx/10)
        x_range_c = (coordX[0] + 4.5*dx/10, coordX[0] + 5.5*dx/10)
        x_range_r = (coordX[0] + 9*dx/10, coordX[0] + 10*dx/10)
    
        y_range_b = (coordY[0], coordY[0] + dy/10)
        y_range_c = (coordY[0] + 4.5*dy/10, coordY[0] + 5.5*dy/10)
        y_range_t = (coordY[0] + 9*dy/10, coordY[0] + 10*dy/10)
    
        kw['key'] = 'r'    
        vxS_lb = scheme.getVoxelScenario(x_range_l, y_range_b)
        vxS_cb = scheme.getVoxelScenario(x_range_c, y_range_b)
        vxS_rb = scheme.getVoxelScenario(x_range_r, y_range_b)
        vxS_lc = scheme.getVoxelScenario(x_range_l, y_range_c)
        vxS_cc = scheme.getVoxelScenario(x_range_c, y_range_c)
        vxS_rc = scheme.getVoxelScenario(x_range_r, y_range_c)
        vxS_lt = scheme.getVoxelScenario(x_range_l, y_range_t)
        vxS_ct = scheme.getVoxelScenario(x_range_c, y_range_t)
        vxS_rt = scheme.getVoxelScenario(x_range_r, y_range_t)
    
        refInput = {}
        refInput['lb'] = _calLinkAtten(cal, vxS_lb, **kw)
        refInput['cb'] = _calLinkAtten(cal, vxS_cb, **kw)
        refInput['rb'] = _calLinkAtten(cal, vxS_rb, **kw)
        refInput['lc'] = _calLinkAtten(cal, vxS_lc, **kw)
        refInput['cc'] = _calLinkAtten(cal, vxS_cc, **kw)
        refInput['rc'] = _calLinkAtten(cal, vxS_rc, **kw)
        refInput['lt'] = _calLinkAtten(cal, vxS_lt, **kw)
        refInput['ct'] = _calLinkAtten(cal, vxS_ct, **kw)
        refInput['rt'] = _calLinkAtten(cal, vxS_rt, **kw)
    
        return refInput
    else:
        raise ValueError('input not defined')

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