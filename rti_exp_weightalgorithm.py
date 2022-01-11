# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 10:01:53 2022

@author: krong
"""
from rti_eval import RTIEvaluation, RecordIndex
from rti_sim_input import simulateInput, reference_object_position

def process_weightalgorithm(sim):
    """
    This process investigates sensor number.

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
        'title':'weightalgorithm',
        'area_dimension':(10.,10.),
        'voxel_dimension':(0.25,0.25),
        'sensing_area_position':(9.,9.),
        # 'n_sensor':20,
        'alpha': 1, 
        'schemeType':'SW',
        # 'weightalgorithm':'LS',
        'object_dimension': (1., 1.),
        #sample setting        
        # 'SNR':10,
        # 'SNR_mode' : 2,
        # 'sample_size' : 100,
        #input setting
        'paramset': ['weightalgorithm'],
        'paramlabel': ['Weighting Algorithm'],
        'param1' : ['LS1', 'LS2', 'EL', 'EX', 'IN'],
        # 'param2' : [1e1, 1e2, 1e3, 1e4],
        #output setting
        'gfx_enabled' : False,
        'record_enabled' : False,
        'resultset':[
            RecordIndex.RMSE_ALL,
            RecordIndex.OBJ_RATIO,
            RecordIndex.OBJ_MEAN,
            RecordIndex.NON_MEAN,
            RecordIndex.DERIVATIVE_BORDERRATIO,
            RecordIndex.DERIVATIVE_NONBORDERRATIO,
            RecordIndex.DERIVATIVE_RATIO_BN]
        }     

    obj_dim = setting['object_dimension']
    
    ev = RTIEvaluation(**setting)
    
    for idx, w in enumerate(ev.param1):
        savepath = sim.process_routine(weightalgorithm=w, **setting)
        # for idx_snr, sn in enumerate(ev.param2):
            # check each snr
        obj_pos = reference_object_position(sim.coorD(), ['cc'], obj_dim)
        refInput = simulateInput(sim.scheme,
                         sim.calculator,
                         obj_pos[0],
                          # SNR = sn,
                         form = 'cc',
                         **setting)
        for key, value in refInput.items():
            # calculate image
            iM = (sim.estimator.calVoxelAtten(value[0], True))
            # result evaluation
            ev.evaluate(sim,                        # RTI Simulation
                        value[0],                   # Link Attenuation
                        value[1],                   # Reference
                        iM,                         # Image
                        savepath,                   # Result Folder
                        key,                        # Information of sample
                        # data index
                        data_idx1 = idx,            # data index 1
                        # data_idx2 = idx_snr,        # data index 2
                        # data_idx3 = value[2],       # data index 3
                        # adding title
                        add_title = w)
    # conclude the results
    ev.conclude(savepath['conc'], setting, 
                # add_title = f's@{setting["sample_size"]}',
                gfx = 'plot')