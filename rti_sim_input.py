# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 09:11:05 2021

@author: krong
"""
from rti_grid import RTIGrid

def simulateInput(scheme, calculator, obj_pos, obj_dim=(1.,1.), **kw):
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

    Returns
    -------
    refInput : dictionary
        reference input in form of pixel matrix

    """
    
    
    x_range = (obj_pos[0], obj_pos[0] + obj_dim[0])
    y_range = (obj_pos[1], obj_pos[1] + obj_dim[1])
    
    vxS = scheme.getVoxelScenario(x_range, y_range)
    l_Atten = _calIdealLinkAtten(calculator, vxS)
    if 'snr' in kw:
        l_Atten = _calCorruptedLinkAtten(l_Atten)
    refInput = {}
    k = 'o(' + str(obj_pos[0]) + ',' + str(obj_pos[1]) + ')'
    refInput[k] = [l_Atten, vxS]
    
    return refInput
    

def simulateFormInput(sim, formSet, objXLength = 0, objYLength = 0):
    """
    Parameters
    ----------
    sim : RTISimulation
    form_set : String
        'reference' generate input at 9 reference position
        | lt | ct | rt |
        | lc | cc | rc |
        | lb | cb | rb |
        'center' stand at the center of the area
        ...
        'Pass Center' Moving through the center
    objWidth : Numerical
        DESCRIPTION.
    objLength : Numerical
        DESCRIPTION.
    snr : Numerical Value
        Signal-to-Noise ratio 
        The default is 0. (No additive noise)

    Returns
    -------
    None.

    """
    scheme = sim.scheme
    wc = sim.calculator

    coordX = scheme.selection.coordX
    coordY = scheme.selection.coordY

    dx = coordX[-1] - coordX[0]
    dy = coordY[-1] - coordY[0]

    if formSet == 'center':

        center_x = coordX[0] + dx/2
        center_y = coordY[0] + dy/2

        x_range = (center_x - objXLength/2, center_x + objXLength/2)
        y_range = (center_y - objYLength/2, center_y + objYLength/2)

        vxS = scheme.getVoxelScenario(x_range, y_range)
        l_Atten = _calIdealLinkAtten(sim.calculator, vxS)

        refInput = {}
        refInput['center'] = [l_Atten, vxS]

        return refInput
    
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

    l_lb = _calIdealLinkAtten(wc, vxS_lb)
    l_cb = _calIdealLinkAtten(wc, vxS_cb)
    l_rb = _calIdealLinkAtten(wc, vxS_rb)
    l_lc = _calIdealLinkAtten(wc, vxS_lc)
    l_cc = _calIdealLinkAtten(wc, vxS_cc)
    l_rc = _calIdealLinkAtten(wc, vxS_rc)
    l_lt = _calIdealLinkAtten(wc, vxS_lt)
    l_ct = _calIdealLinkAtten(wc, vxS_ct)
    l_rt = _calIdealLinkAtten(wc, vxS_rt)

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
    l : TYPE
        DESCRIPTION.
    SNR : float
        Ratio of signal mean and noise sigma    

    Returns
    -------
    Link Attenuation with additive noise

    """
    pass
            
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