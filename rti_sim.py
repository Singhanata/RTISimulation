"""
Created on Thu Jun  3 18:44:39 2021

@author: krong
"""

import numpy as np
from math import ceil

import os
from datetime import datetime

from rti_util import Position
from rti_estimator import RTIEstimator
from rti_eval import RMSEEvaluation as calRMSE
from rti_eval import derivativeEval as calDerivative
from rti_grid import RTIGrid
from rti_scheme_sideposition import SidePositionScheme
from rti_scheme_rectangular import RectangularScheme
from rti_sim_input import simulateInput
from rti_cal_linesegment import LineWeightingRTICalculator
from rti_cal_ellipse import EllipseRTICalculator
from rti_cal_expdecay import ExpDecayRTICalculator
from rti_cal_invarea import InvAreaRTICalculator

from rti_plot import plotRTIIm, plotSurface, plotDerivative

class RTISimulation():
    def __init__(self):
        tStr = datetime.now().strftime('-%d%m%Y-%H%M%S')
        res_dir = 'results/results' + tStr
        os.getcwd()
        try:
            os.mkdir(res_dir)
        except:
            print('Folder ' + res_dir + ' is already exist')
        self.res_dir = res_dir

    def getTitle(self, delimiter=',', short = False):
        if short:
            setting = self.estimator.weightCalculator.getSetting()
            title_w = f'W{setting["Width"]}' + delimiter
            title_l = f'L{setting["Length"]}' + delimiter
            title_vx = f'VX{setting["Voxel Width"]}' + delimiter
            title_SC = f'SC{setting["Sensor Count"]}' 
            title_SR = delimiter
            title_sch = setting['scheme'] + '-'
            title_cal = setting['WeightAlgorithm']
        else:
            setting = self.estimator.weightCalculator.getSetting()
            title_w = f'W@{setting["Width"]}' + delimiter
            title_l = f'L@{setting["Length"]}' + delimiter
            title_vx = f'VX@{setting["Voxel Width"]}' + delimiter
            title_SC = f'SC@{setting["Sensor Count"]}' + '-'
            title_SR = f'SR@{setting["Length"]/(setting["Sensor Count"]/2)}' + delimiter
            title_sch = setting['scheme'] + '-'
            title_cal = setting['WeightAlgorithm']

        return (title_w + title_l +
                title_vx + title_SC + title_SR + title_sch + title_cal)

    def process_routine(self, **kw):
        l_area = 10
        if 'l_area' in kw:
            l_area = kw['l_area']
        w_area = 10
        if 'w_area' in kw:
            w_area = kw['w_area']
        vx_dim = 0.5
        if 'vx_dim' in kw:
            vx_dim = kw['vx_dim']
        n_sensor = 20
        if 'n_sensor' in kw:
            n_sensor = kw['n_sensor']
        ref_pos = Position(0., 0.)
        if 'ref_pos' in kw:
            ref_pos = kw['ref_pos']
        schemeType = 'SW'
        if 'schemeType' in kw:
            schemeType = kw['schemeType']
        weightalgorithm = 'EL'
        if 'weightalgorithm' in kw:
            weightalgorithm = kw['weightalgorithm']

        if schemeType == 'SW':
            self.scheme = SidePositionScheme(ref_pos,
                                             w_area,      # area_width
                                             l_area,      # area_length
                                             vx_dim,      # vx_width
                                             vx_dim,      # vx_length
                                             w_area,      # wa_width
                                             l_area,      # wa_length
                                             n_sensor)    # n_sensor
        elif schemeType == 'RE':
            self.scheme = RectangularScheme(ref_pos,
                                            w_area,       # area_width
                                            l_area,       # area_length
                                            vx_dim,       # vx_width
                                            vx_dim,       # vx_length
                                            w_area,       # wa_width
                                            l_area,       # wa_length
                                            n_sensor)     # n_sensor
        else:
            ValueError('Scheme Type not exist')

        if weightalgorithm == 'LS':
            if 'cal_mode' in kw:
                self.calculator = LineWeightingRTICalculator(self.scheme,
                                                             kw['cal_mode'])
            else:
                self.calculator = LineWeightingRTICalculator(self.scheme)
        elif weightalgorithm == 'EL':
            if 'lambda_coeff' in kw:
                self.calculator = EllipseRTICalculator(self.scheme,
                                                       kw['lambda_coeff'])
            else:
                self.calculator = EllipseRTICalculator(self.scheme)
        elif weightalgorithm == 'EX':
            if 'sigma_w' in kw:
                self.calculator = ExpDecayRTICalculator(self.scheme,
                                                        kw['sigma_w'])
            else:
                self.calculator = ExpDecayRTICalculator(self.scheme)
        elif weightalgorithm == 'IN':
            if 'lambda_min' in kw:
                self.calculator = InvAreaRTICalculator(self.scheme,
                                                       kw['lambda_min'])
            else:
                self.calculator = InvAreaRTICalculator(self.scheme)
        else:
            ValueError('Weighting Algorithm not exist')

        if 'alpha' in kw:
            self.estimator = RTIEstimator(self.calculator,
                                          kw['alpha'])
        else:
            self.estimator = RTIEstimator(self.calculator)

        res_folder = self.res_dir + '/' + self.getTitle('', True)
        try:
            os.mkdir(res_folder)
        except:
            print('Folder ' + res_folder + ' is already exist')

        return res_folder

    def process_showPositionFactor(self):
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

        fdn = self.process_routine(l_area=10,
                                   w_area=10,
                                   vx_dim=0.5,
                                   n_sensor=20,
                                   schemeType='SW',
                                   weightalgorithm='EX')

        end_nx = ceil(obj_dim_x / self.scheme.vx_width)
        end_ny = ceil(obj_dim_y / self.scheme.vx_length)
        
        c_offset_x = ceil(end_nx/2)
        c_offset_y = ceil(end_ny/2)

        x_exp_coorD = np.asarray(self.scheme.coordX[0:-end_nx])
        y_exp_coorD = np.asarray(self.scheme.coordY[0:-end_ny])

        c_rmse = np.zeros((len(x_exp_coorD), len(y_exp_coorD)))
        shape = self.scheme.getShape()

        fn_fig = fdn + '/fig'
        try:
            os.mkdir(fn_fig)
        except:
            print('Folder ' + fn_fig + ' is already exist')
        fn_fig += '/' + self.getTitle('',True)

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

        pre_fn = self.getTitle('', True)

        for i in range(len(x_exp_coorD)):
            for j in range(len(y_exp_coorD)):
                x = x_exp_coorD[i]
                y = y_exp_coorD[j]
                
                c_x_idx = i + c_offset_x
                c_y_idx = j + c_offset_y

                refInput = simulateInput(self.scheme,
                                         self.calculator,
                                         (x, y),
                                         (obj_dim_x, obj_dim_y))
                for key, value in refInput.items():
                    imA = (self.estimator.calVoxelAtten(value[0]))
                    iM = (RTIGrid.reshapeVoxelArr2Im(imA, shape))
                    r = calRMSE(value[1], iM)
                    de = calDerivative(value[1], 
                                       iM, 
                                       indexOfInterest = (c_x_idx, c_y_idx))
                    c_rmse[i][j] = r['rmse_all']

                    if s_graphic:
                        fn_f = fn_fig + '-' + key
                        title = pre_fn + '-' + key
                        plotRTIIm(self.scheme,
                                  iM, 
                                  path = fn_f,
                                  title = self.getTitle(), 
                                  label = 'Rel. Attenuation',  
                                  rmse = r['rmse_all'])
                        plotDerivative(self.scheme,
                                       de,
                                       path = fn_f,
                                       title = self.getTitle(),
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
        plotRTIIm(self.scheme,
                  c_rmse,
                  path = fn_cg,
                  title = title, 
                  label = 'RMSE',  
                  color = 'tab20')
        
        if s_surface:
            plotSurface(self.scheme,
                          c_rmse,
                          path = fn_cg,
                          title = title, 
                          label = 'RMSE',  
                          color = 'tab20')
            
