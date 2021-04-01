from geoutil import Position, RTIGrid
from rti_scheme import SidePositionScheme
from rti_cal import LineWeightingRTICalculator
from rti_estimator import RTIEstimator
from rti_eval import RMSEEvaluation as calRMSE
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

class RTISimulation():
    def __init__(self):
        pass
    
    def calIdealLinkAtten(self, voxelAttenM):
        try:
            vxArr = RTIGrid.reshapeVoxelM2Arr(voxelAttenM)
            linkAttenArr = (self.
                            estimator.
                            weightCalculator.
                            calIdealLinkAtten(vxArr))
            return linkAttenArr
        except ValueError:
            raise ValueError('Dimension mismatch.')

    def simulateReferenceInput(self):
        scheme = self.estimator.weightCalculator.scheme

        coordX = scheme.selection.coordX
        coordY = scheme.selection.coordY

        dx = coordX[-1] - coordX[0]
        dy = coordY[-1] - coordY[0]

        x_range_l = (coordX[0], coordX[0] + dx/5)
        x_range_c = (coordX[0] + 2*dx/5, coordX[0] + 3*dx/5)
        x_range_r = (coordX[0] + 4*dx/5, coordX[0] + 5*dx/5)

        y_range_b = (coordY[0], coordY[0] + dy/5)
        y_range_c = (coordY[0] + 2*dy/5, coordY[0] + 3*dy/5)
        y_range_t = (coordY[0] + 4*dy/5, coordY[0] + 5*dy/5)

        vxS_lb = scheme.getVoxelScenario(x_range_l, y_range_b)
        vxS_cb = scheme.getVoxelScenario(x_range_c, y_range_b)
        vxS_rb = scheme.getVoxelScenario(x_range_r, y_range_b)
        vxS_lc = scheme.getVoxelScenario(x_range_l, y_range_c)
        vxS_cc = scheme.getVoxelScenario(x_range_c, y_range_c)
        vxS_rc = scheme.getVoxelScenario(x_range_r, y_range_c)
        vxS_lt = scheme.getVoxelScenario(x_range_l, y_range_t)
        vxS_ct = scheme.getVoxelScenario(x_range_c, y_range_t)
        vxS_rt = scheme.getVoxelScenario(x_range_r, y_range_t)

        l_lb = self.calIdealLinkAtten(vxS_lb)
        l_cb = self.calIdealLinkAtten(vxS_cb)
        l_rb = self.calIdealLinkAtten(vxS_rb)
        l_lc = self.calIdealLinkAtten(vxS_lc)
        l_cc = self.calIdealLinkAtten(vxS_cc)
        l_rc = self.calIdealLinkAtten(vxS_rc)
        l_lt = self.calIdealLinkAtten(vxS_lt)
        l_ct = self.calIdealLinkAtten(vxS_ct)
        l_rt = self.calIdealLinkAtten(vxS_rt)

        refInput = {}
        refInput['lb'] = [l_lb, vxS_lb]
        refInput['cb'] = [l_cb, vxS_cb]
        refInput['rb'] = [l_rb, vxS_rb]
        refInput['lc'] = [l_lc, vxS_lc]
        refInput['cc'] = [l_cc, vxS_cc]
        refInput['rc'] = [l_rc, vxS_rc]
        refInput['lt'] = [l_lt, vxS_lt]
        refInput['ct'] = [l_ct, vxS_ct]
        refInput['rt'] = [l_rt, vxS_rt]

        return refInput
    
    def simulateInput(self, formSet, objXLength, objYLength):
        """
        Parameters
        ----------
        form_set : String
            'centre' stand at the center of the area
            'Left' stand at the left side
            ...
            'Pass Center' Moving through the center
        objWidth : Numerical
            DESCRIPTION.
        objLength : Numerical
            DESCRIPTION.

        Returns
        -------
        None.

        """
        scheme = self.estimator.weightCalculator.scheme

        coordX = scheme.selection.coordX
        coordY = scheme.selection.coordY
        
        dx = coordX[-1] - coordX[0]
        dy = coordY[-1] - coordY[0]

        if formSet == 'center':

            center_x = coordX[0] + dx/2
            center_y = coordY[0] + dy/2
        
            x_range = (center_x - objXLength/2, center_x + objXLength/2)
            y_range = (center_y - objYLength/2, center_y + objYLength/2)
        
            vxS = scheme.getVoxelScenario(x_range, y_range)
            l_Atten = self.calIdealLinkAtten(vxS)
            
            refInput = {}
            refInput['center'] = l_Atten
            
            return refInput
        return self.simulateReferenceInput()

    def plotRTIIm(self, iM, sensorPostion, path, title, rmse):
        sel = self.estimator.weightCalculator.scheme.selection

        coordX = sel.coordX
        coordY = sel.coordY

        fig,ax = plt.subplots(1,1)
        hm = ax.imshow(iM.T,
                       extent = [coordX[0], coordX[-1], coordY[0], coordY[-1]],
                       cmap = 'coolwarm',
                       origin = 'lower',
                       interpolation = 'nearest',
                       vmin = 0)
        ax.set_title(title, pad=10)
        ax.set_xlabel('RMSE =' + str(rmse))
        plt.colorbar(hm)
        plt.scatter(sensorPostion[0], sensorPostion[1], s=200, c = 'black')
        plt.grid()
        fn = path + '.svg'
        plt.savefig(fn)
        plt.show()

    def getTitle(self):
        setting = self.estimator.weightCalculator.scheme.getSetting()
        title_w = f'w@{setting["Width"]}' + ', '
        title_l = f'l@{setting["Length"]}' + ', '
        title_vx = f'VX@{setting["Voxel Width"]}' + ', '
        title_SC = f'SC@{setting["Sensor Count"]}' + '-'
        title_SR = f'SR@{setting["Length"]/(setting["Sensor Count"]/2)}'

        return title_w + title_l + title_vx + title_SC + title_SR

    def process_default(self):
        lengtH = np.linspace(10.,100., 10)  # Lenght in [m]
        widtH = [5, 10, 20, 50, 100]        # Width in [m]
        sensor_ratio = [0.5, 0.25, 0.1, 1, 2, 4, 10]    # Lenght/Sensor in [m/unit]
        vX = [0.5, 0.25, 0.1, 1]            # Voxel Length in [m]
        tStr = datetime.now().strftime('-%d%m%Y-%H%M%S')
        res_dir ='results' + tStr
        os.getcwd()
        try:
            os.mkdir(res_dir)
        except:
            print('Folder ' + res_dir + ' is already exist')
        for l in lengtH:
            for w in widtH:
                if l < w:
                    continue
                for sr in sensor_ratio:
                    n = int((1/sr) * l) * 2
                    if n < 4:
                        continue
                    for vx in vX:
                        rs = SidePositionScheme(Position(0.,0.),
                                                    w,      # area_width
                                                    l,      # area_length
                                                    vx,     # vx_width
                                                    vx,     # vx_length
                                                    n,      # n_sensor
                                                    w,      # wa_width
                                                    l)      # wa_length
                        rc = LineWeightingRTICalculator(rs)
                        re = RTIEstimator(rc, 1.)
                        self.estimator = re
                        selection = (self.
                                     estimator.
                                     weightCalculator.
                                     scheme.
                                     selection)
                        refInput = self.simulateReferenceInput()
                        for key, value in refInput.items():
                            imA = (self.
                                   estimator.
                                   calVoxelAtten(value[0]))
                            iM = (RTIGrid.
                                  reshapeVoxelArr2Im(imA,
                                                     selection.getShape()))
                            fn = res_dir + '/' + self.getTitle() + '-' + key
                            rmse = calRMSE(value[1], iM)
                            title = self.getTitle() + '-' + key 
                        
                            sP = rs.getSensorPosition() 
 
                            self.plotRTIIm(iM, sP, fn, title, rmse)
                            
    def process_scenario(self):
        l_area = 10
        w_area = 6
        vx_dim = 1
        n_sensor = 20
        obj_dim_x = 4
        obj_dim_y = 2
        
        tStr = datetime.now().strftime('-%d%m%Y-%H%M%S')
        res_dir ='results' + tStr
        os.getcwd()
        try:
            os.mkdir(res_dir)
        except:
            print('Folder ' + res_dir + ' is already exist')
        rs = SidePositionScheme(Position(0.,0.),
                                w_area,      # area_width
                                l_area,      # area_length
                                vx_dim,     # vx_width
                                vx_dim,     # vx_length
                                n_sensor,      # n_sensor
                                w_area,      # wa_width
                                l_area)      # wa_length
        rc = LineWeightingRTICalculator(rs)
        re = RTIEstimator(rc, 1.)
        self.estimator = re
        selection = (self.
                     estimator.
                     weightCalculator.
                     scheme.
                     selection)
        refInput = self.simulateInput('center', obj_dim_x, obj_dim_y)
        for key, value in refInput.items():
            imA = (self.
                   estimator.
                   calVoxelAtten(value[0]))
            iM = (RTIGrid.
                  reshapeVoxelArr2Im(imA,
                                     selection.getShape()))
            fn = res_dir + '/' + self.getTitle() + '-' + key
            rmse = calRMSE(value[1], iM)
            title = self.getTitle() + '-' + key                        
            sP = rs.getSensorPosition()
            
            self.plotRTIIm(iM, sP, fn, title, rmse)
                    
        
        
        



