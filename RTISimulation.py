from geoutil import Position, RTIGrid
from rti_scheme import RTIScheme, SidePositionScheme
from rti_cal import RTIWeightCalculator, LineWeightingRTICalculator
from rti_estimator import RTIEstimator
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

class RTISimulation():
    def __init__(self):
        rs = SidePositionScheme()
        rc = LineWeightingRTICalculator(rs)
        re = RTIEstimator(rc, 1.)
        self.estimator = re

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
        w_x_range = dx/5
        w_y_range = dy/5

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
        refInput['lb'] = l_lb
        refInput['cb'] = l_cb
        refInput['rb'] = l_rb
        refInput['lc'] = l_lc
        refInput['cc'] = l_cc
        refInput['rc'] = l_rc
        refInput['lt'] = l_lt
        refInput['ct'] = l_ct
        refInput['rt'] = l_rt

        return refInput

    def plotRTIIm(self, iM, title):
        fig,ax = plt.subplots()
        hm = ax.imshow(iM, cmap = 'coolwarm', interpolation = 'nearest')
        ax.set_title(title)
        plt.colorbar(hm)
        plt.grid()
        fn = title + '.svg'
        plt.savefig(fn)
        plt.show()

    def getTitle(self):
        setting = self.estimator.weightCalculator.scheme.getSetting()
        title_w = f'w@{setting["Width"]}' + ', '
        title_l = f'l@{setting["Length"]}' + ', '
        title_SD = f'SD@{setting["Sensor Distance"]}' + ', '
        title_SC = f'SC@{setting["Sensor Count"]}'

        return title_w + title_l + title_SD + title_SC

    def process(self):
        lengtH = np.linspace(10.,100., 10)
        widtH = [5, 10, 20, 50, 100]
        sensor_ratio = [0.5, 0.25, 0.1, 1, 2, 4, 10]
        vX = [0.5, 0.25, 0.1, 1]
        tStr = datetime.now().strftime('-%d%m%Y-%H%M%S')
        res_dir ='results' + tStr
        os.getcwd()
        try:
            os.mkdir(res_dir)
        except:
            print('Folder ' + res_dir + ' is already exist')
        for l in lengtH:
            for w in widtH:
                if w < l:
                    continue
                for sr in sensor_ratio:
                    n = (1/sr)*l
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
                                   calVoxelAtten(value))
                            iM = (RTIGrid.
                                  reshapeVoxelArr2Im(imA,
                                                     selection.getShape()))
                            fn = res_dir + '/' + self.getTitle() + '-' + key
                            RTISimulation.plotRTIIm(iM, fn)



