# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 11:45:15 2021

@author: krong
"""


from rti_eval import RTIEvaluation, RecordIndex
from rti_sim_input import reference_object_position, simulateInput

def process_alpha(sim):
    """
    Investigation of alpha parameter in RTI Estimator
    Question:
        1. Is alpha related to RMSE
        2. which alpha make the best clarity of the object image
        3. How system react to gaussian noise as alpha changed

    Parameters
    ----------
    sim : Instance of RTISimulation
        

    Returns
    -------
    None.

    """
    setting = {
        #scenario setting
        'title':'alpha',
        'area_dimension':(10.,10.),
        'voxel_dimension':(0.25,0.25),
        'sensing_area_position':(9.,9.),
        'n_sensor':20,
        # 'alpha' : 1,
        'schemeType':'SW',
        'weightalgorithm':'LS1',
        'object_dimension': (1., 1.),
        #sample setting        
        # 'SNR':10,
        'SNR_mode' : 2,
        'sample_size' : 100,
        #input setting
        'paramset': ['alpha', 'snr'],
        'paramlabel': [r'$\alpha$', 'SNR'],
        'param1' : [0.01, 1, 1e2, 1e4],
        'param2' : [1e1, 1e2, 1e3, 1e4],
        #output setting
        'gfx_enabled' : True,
        'record_enabled':False,
        'resultset':[
            RecordIndex.RMSE_ALL,
            RecordIndex.OBJ_RATIO,
            RecordIndex.DERIVATIVE_BORDERRATIO,
            RecordIndex.DERIVATIVE_NONBORDERRATIO,
            RecordIndex.DERIVATIVE_RATIO_BN]
        }
     
    
    ev = RTIEvaluation(**setting)
    
    for idx, al in enumerate(ev.param1):
        # check each alpha 
        savepath = sim.process_routine(alpha = al, **setting)
        for idx_snr, sn in enumerate(ev.param2):
            # check each snr
            obj_pos = reference_object_position(sim.coorD(), ['cc'], 
                                                setting['object_dimension'])
            refInput = simulateInput(sim.scheme,
                             sim.calculator,
                             obj_pos[0],
                              SNR = sn,
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
                            data_idx2 = idx_snr,        # data index 2
                            data_idx3 = value[2],       # data index 3
                            # adding title
                            add_title = r'$\alpha$' + '@' + str(al))
    # conclude the results
    ev.conclude(savepath['conc'], setting, 
                add_title = f's@{setting["sample_size"]}',
                gfx = 'boxplot')