# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 11:45:15 2021

@author: krong
"""

import numpy as np
import os

from rti_eval import RMSEEvaluation as calRMSE
from rti_eval import derivativeEval as calDerivative
from rti_rec import result_record

from rti_sim_input import simulateInput
from rti_plot import plotRTIIm, plotDerivative

def process_alpha(sim):
    
    s_graphic = True
    s_rec = True
    
    obj_dim_x = 1
    obj_dim_y = 1
    snr = [1, 10, 100, 1000]
    sample_size = 100
    alp = [0.01, 0.1, 1., 10., 100]
    rmse = np.zeros((len(alp), len(snr), sample_size))
    der_border = np.zeros((len(alp), len(snr), sample_size))
    der_borderratio = np.zeros((len(alp), len(snr), sample_size))
    der_nonborder = np.zeros((len(alp), len(snr), sample_size))
    der_nonborderratio = np.zeros((len(alp), len(snr), sample_size))
    for idx, al in enumerate(alp):
        # check each alpha 
        savepath = sim.process_routine(l_area=10,
                                   w_area=10,
                                   vx_dim=0.5,
                                   n_sensor=20,
                                   schemeType='SW',
                                   weightalgorithm='LS',
                                   alpha=al,
                                   add_title='alpha')
        record = {}
        record['x'] = np.asarray(sim.scheme.selection.coordX)
        record['y'] = np.asarray(sim.scheme.selection.coordY) 
        for idx_snr, sn in enumerate(snr):
            # check each snr
            refInput = simulateInput(sim.scheme,
                             sim.calculator,
                             (obj_dim_x, obj_dim_y),
                             form = 'cc',
                             snr = sn,
                             sample_size = sample_size,
                             mode = 2)
            for key, value in refInput.items():
                iM = (sim.estimator.calVoxelAtten(value[0]))
                r = calRMSE(value[1], iM)
                de = calDerivative(value[1], 
                                   iM, 
                                   obj_pos = (4.5, 4.5),
                                   obj_dim = (1., 1.))
                record['ref'] = value[1]
                record['image'] = iM
                record['rmse'] = r
                record['derivative'] = de
                if s_graphic:
                    gfx_name = sim.getTitle('', True) + '_' + key
                    fn_f = os.sep.join([savepath['gfx'], gfx_name])
                    plotRTIIm(sim.scheme,
                              iM, 
                              path = fn_f,
                              title = sim.getTitle(), 
                              label = 'Rel. Attenuation',  
                              rmse = r['rmse_all'])
                    plotDerivative(sim.scheme,
                                   de,
                                   path = fn_f,
                                   title = sim.getTitle(),
                                   label = 'Derivative of Attenuation',
                                   caption = 'border@' 
                                   + '{:.3f}'.format(de['border'])
                                   + ', '
                                   + 'non-border@' 
                                   + '{:.3f}'.format(de['non-border']))
                if s_rec:
                    result_record(savepath['rec'], key, record)
                rmse[idx][idx_snr][value[2]] = r['rmse_all']
                der_border[idx][idx_snr][value[2]] = de['border']
                der_borderratio[idx][idx_snr][value[2]] = de['border_ratio']
                der_nonborder[idx][idx_snr][value[2]] = de['non-border']
                der_nonborderratio[idx][idx_snr][value[2]] = de['non-border_ratio']

        # fig, ax = plt.subplots(1, 1)
        # plt.plot(alp, c_rmse)
        # plt.grid()
        # plt.show()
