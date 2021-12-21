# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 11:45:15 2021

@author: krong
"""

import numpy as np
import os

from rti_eval import RMSEEvaluation as calRMSE
from rti_eval import derivativeEval as calDerivative
from rti_grid import RTIGrid

from rti_sim_input import simulateInput
from rti_plot import plotRTIIm, plotDerivative

import matplotlib.pyplot as plt

def process_alpha(sim):
    
    s_graphic = True
    s_rec = True
    
    obj_dim_x = 1
    obj_dim_y = 1

    alp = [0.01, 0.1, 1., 10., 100]
    c_rmse = np.zeros(len(alp))
    for idx, al in enumerate(alp):
        fdn = sim.process_routine(l_area=10,
                                   w_area=10,
                                   vx_dim=0.5,
                                   n_sensor=20,
                                   schemeType='SW',
                                   weightalgorithm='LS',
                                   alpha=al,
                                   add_title='alpha')
        coordX = np.asarray(sim.scheme.selection.coordX)
        coordY = np.asarray(sim.scheme.selection.coordY) 
        fn_fig = fdn + '/fig'
        try:
            os.mkdir(fn_fig)
        except:
            print('Folder ' + fn_fig + ' is already exist')
        fn_fig += '/' + sim.getTitle('', True)
        fn_rec = fdn + '/rec'
        try:
            os.mkdir(fn_rec)
        except:
            print('Folder ' + fn_rec + ' is already exist')
        fn_con = fdn + '/conc'
        try:
            os.mkdir(fn_con)
        except:
            print('Folder ' + fn_con + ' is already exist')
    
        pre_fn = sim.getTitle('', True)
        refInput = simulateInput(sim.scheme,
                         sim.calculator,
                         (obj_dim_x, obj_dim_y),
                         form = 'center',
                         snr = 10,
                         sample_size = 100)
        for key, value in refInput.items():
            imA = (sim.estimator.calVoxelAtten(value[0]))
            iM = (RTIGrid.reshapeVoxelArr2Im(imA, sim.scheme.getShape()))
            r = calRMSE(value[1], iM)
            de = calDerivative(value[1], 
                               iM, 
                               obj_pos = (4.5, 4.5),
                               obj_dim = (1., 1.))
            c_rmse[idx] = r['rmse_all']
            if s_graphic:
                fn_f = fn_fig + '-' + key
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
                               caption = 'obj@' 
                               + '{:.3f}'.format(de['obj-derivative'])
                               + ', '
                               + 'non@' 
                               + '{:.3f}'.format(de['non-derivative']))
            if s_rec:
                fn_r = fn_rec + '/' + key
                try:
                    os.mkdir(fn_r)
                except:
                    print('Folder ' + fn_r + ' is already exist')

                fn_rx = fn_r + '/x.csv'
                fn_ry = fn_r + '/y.csv'
                fn_ref = fn_r + '/ref.csv'
                fn_res = fn_r + '/res.csv'
                fn_info = fn_r + '/info.csv'
                fn_der_x = fn_r + '/derivative_x.csv'
                fn_der_y = fn_r + '/derivative_y.csv'
                fn_der_abs = fn_r + '/derivative_abs.csv'

                np.savetxt(fn_rx, coordX, delimiter=',')
                np.savetxt(fn_ry, coordY, delimiter=',')
                np.savetxt(fn_ref, value[1], delimiter=',')
                np.savetxt(fn_res, iM, delimiter=',')
                np.savetxt(fn_der_x, de['x'],delimiter=',')
                np.savetxt(fn_der_y, de['y'],delimiter=',')
                np.savetxt(fn_der_abs, de['abs'],delimiter=',')
                with open(fn_info, 'w') as f:
                    f.write(pre_fn + '\nRMSE = ' + str(r['rmse_all'])
                + '\nAVG. OBJ. RMSE ,' + str(r['rmse_obj'])
                + '\nAVG. NON. RMSE ,' + str(r['rmse_non'])
                + '\nAVG. OBJ. Attenuation ,' + str(r['obj_mean'])
                + '\nAVG. NON. Attenuation ,' + str(r['non_mean'])
                + '\nAVG.')
                
    fig, ax = plt.subplots(1, 1)
    plt.plot(alp, c_rmse)
    plt.grid()
    plt.show()
