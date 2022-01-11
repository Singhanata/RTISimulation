# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 09:54:49 2022

@author: krong
"""
import numpy as np

from rti_eval import RTIEvaluation, RecordIndex
from rti_sim_input import simulateInput, reference_object_position

def process_formfactor(sim):
    """
    This process investigates the form factor of 
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
        'title':'FormFactor',
        'area_dimension':(10.,10.),
        'voxel_dimension':(0.5,0.5),
        'sensing_area_position':(9.,9.),
        'n_sensor':20,
        'alpha': 1, 
        'schemeType':'SW',
        'weightalgorithm':'LS1',
        # 'object_dimension': (1., 1.),
        #sample setting        
        # 'SNR':10,
        # 'SNR_mode' : 2,
        # 'sample_size' : 3,
        #input setting
        'paramset': ['OBJ_SIZE'],
        # 'paramlabel': [],
        'param1' : np.linspace(1,5,5),
        # 'param2' : [0],
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
    ev = RTIEvaluation(**setting)

    for i, x in enumerate(setting['param1']):
        
        obj_dim = (x,x)
        setting['object_dimension'] = obj_dim
        # for j, y in enumerate(setting['param2']):
        obj_pos = reference_object_position(sim.coorD(), ['cc'], obj_dim)
        refInput = simulateInput(sim.scheme,
                         sim.calculator,
                         obj_pos[0],
                         form = 'cc',
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
                        # data_idx2 = idx_snr,        # data index 2
                        # data_idx3 = value[2],       # data index 3
                        # adding title
                        add_title = 'Object Size' + '@' + str(obj_dim)
                        )

    ev.conclude(savepath['conc'], setting, 
                gfx = 'plot',
                # add_title = f's@{setting["sample_size"]}',
                scheme = sim.scheme)