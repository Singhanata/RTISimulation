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
    obj_dim = (1., 1.)
    
    ev = RTIEvaluation(['snr', 'alpha'],
                       ['SNR', r'$\alpha$'],
                         [RecordIndex.RMSE_ALL,
                          RecordIndex.DERIVATIVE_BORDER,
                          RecordIndex.DERIVATIVE_BORDERRATIO,
                          RecordIndex.DERIVATIVE_NONBORDER,
                          RecordIndex.DERIVATIVE_NONBORDERRATIO],
                          param1 = [1, 10, 100, 1000],
                          param2 = [0.01, 0.1, 1, 10, 100],
                          sample_size = 10,
                          gfx_enabled = False,
                          record_enabled=False)
    
    for idx, al in enumerate(ev.param1):
        # check each alpha 
        setting, savepath = sim.process_routine(
                                        area_dimension=(10.,10.),
                                        voxel_dimension=(0.5,0.5),
                                        n_sensor=20,
                                        schemeType='SW',
                                        weightalgorithm='LS',
                                        alpha=al,
                                        title='alpha')
        setting['object_dimension'] = obj_dim
        for idx_snr, sn in enumerate(ev.param2):
            # check each snr
            obj_pos = reference_object_position(sim.coorD(), ['cc'])
            refInput = simulateInput(sim.scheme,
                             sim.calculator,
                             obj_dim,
                             obj_pos[0],
                             snr = sn,
                             sample_size = ev.sample_size,
                             form = 'cc',
                             mode = 2)
            for key, value in refInput.items():
                # calculate image
                iM = (sim.estimator.calVoxelAtten(value[0]))
                # result evaluation
                ev.evaluate(sim,
                            value[0],
                            value[1],
                            iM,
                            (idx, idx_snr, value[2]),
                            key,
                            savepath)
    # conclude the results
    ev.conclude(savepath['conc'], setting)