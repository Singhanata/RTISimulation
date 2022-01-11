# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 08:46:00 2021

@author: krong
"""
import numpy as np
from math import ceil

from rti_eval import RTIEvaluation, RecordIndex
from rti_sim_input import simulateInput

def process_position(sim):
    """
    This process investigates all possible position of an rectangular 
    object in the rectangular detection area.

    Parameters
    ----------
    sim : RTI Simulation Object
        Instance of RTISimulaiton  

    Returns
    -------
    None.

    """
    setting = {
        #scenario setting
        'title':'position',
        'area_dimension':(10.,10.),
        'voxel_dimension':(0.5,0.5),
        'sensing_area_position':(9.,9.),
        'n_sensor':20,
        'alpha': 1, 
        'schemeType':'SW',
        'weightalgorithm':'LS1',
        'object_dimension': (1., 1.),
        #sample setting        
        'SNR':10,
        'SNR_mode' : 2,
        # 'sample_size' : 3,
        #input setting
        'paramset': ['X', 'Y'],
        # 'paramlabel': [],
        # 'param1' : [1e2, 1e4],
        # 'param2' : [10, 100, 1000, 1e4],
        #output setting
        'gfx_enabled' : True,
        'record_enabled':False,
        'resultset':[
            RecordIndex.RMSE_ALL,
            RecordIndex.OBJ_RATIO,
            RecordIndex.DERIVATIVE_BORDERRATIO,
            RecordIndex.DERIVATIVE_NONBORDERRATIO,
            RecordIndex.DERIVATIVE_RATIO_XN,
            RecordIndex.DERIVATIVE_RATIO_YN,
            RecordIndex.DERIVATIVE_RATIO_BN]
        }     

    savepath = sim.process_routine(**setting)
    
    obj_dim = setting['object_dimension']
    end_nx = ceil(obj_dim[0] / sim.scheme.vx_width)
    end_ny = ceil(obj_dim[1] / sim.scheme.vx_length)
    
    x_exp_coorD = np.asarray(sim.scheme.coordX[0:-end_nx])
    y_exp_coorD = np.asarray(sim.scheme.coordY[0:-end_ny])

    x_coorD = [x + obj_dim[0]/2 for x in x_exp_coorD]
    y_coorD = [y + obj_dim[1]/2 for y in y_exp_coorD]

    setting['param1'] = x_coorD
    setting['param2'] = y_coorD
    
    ev = RTIEvaluation(**setting)

    for i, x in enumerate(x_coorD):
        for j, y in enumerate(y_coorD):
            refInput = simulateInput(sim.scheme,
                             sim.calculator,
                             (x, y),
                             **setting)
            for key, value in refInput.items():
                iM = (sim.estimator.calVoxelAtten(value[0], True))
                ev.evaluate(sim,                        # RTI Simulation
                            value[0],                   # Link Attenuation
                            value[1],                   # Reference
                            iM,                         # Image
                            savepath,                   # Result Folder
                            key,                        # Information of sample
                            # data index
                            data_idx1 = i,              # data index 1
                            data_idx2 = j,        # data index 2
                            # data_idx3 = value[2],       # data index 3
                            # adding title
                            # add_title = 'Object Size' + '@' + str(i)
                            )

    ev.conclude(savepath['conc'], setting, 
                gfx = 'imshow',
                # add_title = f'SNR@{setting["SNR"]}s@{setting["sample_size"]}',
                scheme = sim.scheme)
        