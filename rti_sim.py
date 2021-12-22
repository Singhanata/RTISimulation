"""
Created on Thu Jun  3 18:44:39 2021

@author: krong
"""
import os
from datetime import datetime

from rti_util import Position
from rti_estimator import RTIEstimator
from rti_scheme_sideposition import SidePositionScheme
from rti_scheme_rectangular import RectangularScheme
from rti_cal_linesegment import LineWeightingRTICalculator
from rti_cal_ellipse import EllipseRTICalculator
from rti_cal_expdecay import ExpDecayRTICalculator
from rti_cal_invarea import InvAreaRTICalculator

class RTISimulation():
    def __init__(self):
        tStr = datetime.now().strftime('-%d%m%Y-%H%M%S')
        res_dir = os.sep.join(['results',('results'+tStr)])
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
            title_SR = '-'
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

        fdn = self.res_dir
        title = ''
        if 'add_title' in kw:
            title += kw['add_title'] + '-'
        fdn =  os.sep.join([fdn, (title + self.getTitle('', True))]) 
        try:
            os.mkdir(fdn)
        except:
            print('Folder ' + fdn + ' is already exist')
        fn_fig = os.sep.join([fdn, 'fig']) 
        try:
            os.mkdir(fn_fig)
        except:
            print('Folder ' + fn_fig + ' is already exist')
        fn_rec = os.sep.join([fdn, 'rec'])
        try:
            os.mkdir(fn_rec)
        except:
            print('Folder ' + fn_rec + ' is already exist')
        fn_con = os.sep.join([fdn, 'conc'])
        try:
            os.mkdir(fn_con)
        except:
            print('Folder ' + fn_con + ' is already exist')
        
        save_path = {}
        save_path['gfx'] = fn_fig
        save_path['rec'] = fn_rec
        save_path['conc'] = fn_con
        return save_path

    
            
