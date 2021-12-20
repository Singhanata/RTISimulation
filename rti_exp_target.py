# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 08:46:00 2021

@author: krong
"""
import numpy as np
from math import ceil

import os

from rti_eval import RMSEEvaluation as calRMSE
from rti_eval import derivativeEval as calDerivative
from rti_grid import RTIGrid

from rti_sim_input import simulateInput
from rti_plot import plotRTIIm, plotSurface, plotDerivative

def process_showPositionFactor(sim):
    """
    This process investigates all possible position of an rectangular 
    object in the detection area.

    Returns
    -------
    None.

    """
    s_graphic = True
    s_rec = True
    s_surface = False

    obj_dim_x = 4
    obj_dim_y = 4

    fdn = sim.process_routine(l_area=10,
                               w_area=10,
                               vx_dim=0.5,
                               n_sensor=20,
                               schemeType='SW',
                               weightalgorithm='IN')

    end_nx = ceil(obj_dim_x / sim.scheme.vx_width)
    end_ny = ceil(obj_dim_y / sim.scheme.vx_length)
    
    c_offset_x = ceil(end_nx/2)
    c_offset_y = ceil(end_ny/2)

    x_exp_coorD = np.asarray(sim.scheme.coordX[0:-end_nx])
    y_exp_coorD = np.asarray(sim.scheme.coordY[0:-end_ny])

    c_rmse = np.zeros((len(x_exp_coorD), len(y_exp_coorD)))
    shape = sim.scheme.getShape()

    fn_fig = fdn + '/fig'
    try:
        os.mkdir(fn_fig)
    except:
        print('Folder ' + fn_fig + ' is already exist')
    fn_fig += '/' + sim.getTitle('',True)

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

    for i in range(len(x_exp_coorD)):
        for j in range(len(y_exp_coorD)):
            x = x_exp_coorD[i]
            y = y_exp_coorD[j]
            
            c_x_idx = i + c_offset_x
            c_y_idx = j + c_offset_y

            refInput = simulateInput(sim.scheme,
                                     sim.calculator,
                                     (x, y),
                                     (obj_dim_x, obj_dim_y))
            for key, value in refInput.items():
                imA = (sim.estimator.calVoxelAtten(value[0]))
                iM = (RTIGrid.reshapeVoxelArr2Im(imA, shape))
                r = calRMSE(value[1], iM)
                de = calDerivative(value[1], 
                                   iM, 
                                   indexOfInterest = (c_x_idx, c_y_idx))
                c_rmse[i][j] = r['rmse_all']

                if s_graphic:
                    fn_f = fn_fig + '-' + key
                    title = pre_fn + '-' + key
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
                    fn_der_x_interest = (fn_r + '/derivative_x@' 
                                         + str(x + obj_dim_x/2) 
                                         + '.csv') 
                    fn_der_y = fn_r + '/derivative_y.csv'
                    fn_der_y_interest = (fn_r + '/derivative_y@' 
                                         + str(y + obj_dim_y/2) 
                                         + '.csv') 
                    fn_der_abs = fn_r + '/derivative_abs.csv'

                    np.savetxt(fn_rx, x_exp_coorD, delimiter=',')
                    np.savetxt(fn_ry, y_exp_coorD, delimiter=',')
                    np.savetxt(fn_ref, value[1], delimiter=',')
                    np.savetxt(fn_res, iM, delimiter=',')
                    np.savetxt(fn_der_x, de['x'],delimiter=',')
                    np.savetxt(fn_der_x_interest, de['x_interest'], 
                               delimiter=',')
                    np.savetxt(fn_der_y, de['y'],delimiter=',')
                    np.savetxt(fn_der_y_interest, de['y_interest'], 
                               delimiter=',')
                    np.savetxt(fn_der_abs, de['abs'],delimiter=',')
                    with open(fn_info, 'w') as f:
                        f.write(pre_fn + '\nRMSE = ' + str(r['rmse_all'])
                    + '\nAVG. OBJ. RMSE ,' + str(r['rmse_obj'])
                    + '\nAVG. NON. RMSE ,' + str(r['rmse_non'])
                    + '\nAVG. OBJ. Attenuation ,' + str(r['obj_mean'])
                    + '\nAVG. NON. Attenuation ,' + str(r['non_mean'])
                    + '\nAVG.')
                        
    x_exp_coorD = [x + obj_dim_x/2 for x in x_exp_coorD]
    y_exp_coorD = [y + obj_dim_y/2 for y in y_exp_coorD]

    obj_dim_txt = 'obj(' + str(obj_dim_x) + ',' + str(obj_dim_y) + ')'
    fn_cx = fn_con + '/' + obj_dim_txt + '_X_PosExp.csv'
    fn_cy = fn_con + '/' + obj_dim_txt + '_Y_PosExp.csv'
    fn_crmse = fn_con + '/' + obj_dim_txt + '_RMSE_PosExp.csv'
    fn_cg = fn_con + '/' + obj_dim_txt + '_RMSE_PosExp'

    np.savetxt(fn_cx, x_exp_coorD, delimiter=',')
    np.savetxt(fn_cy, y_exp_coorD, delimiter=',')
    np.savetxt(fn_crmse, c_rmse, delimiter=',')

    title = (pre_fn +
             '-' + obj_dim_txt + '-RMSE')
    plotRTIIm(sim.scheme,
              c_rmse,
              path = fn_cg,
              title = title, 
              label = 'RMSE',  
              color = 'tab20')
    
    if s_surface:
        plotSurface(sim.scheme,
                      c_rmse,
                      path = fn_cg,
                      title = title, 
                      label = 'RMSE',  
                      color = 'tab20')