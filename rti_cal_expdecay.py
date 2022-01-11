"""
Created on Thu Jun  3 18:44:39 2021

@author: krong
"""

from rti_cal import RTIWeightCalculator
import numpy as np
import math

class ExpDecayRTICalculator(RTIWeightCalculator):
    def __init__(self, scheme, sigma_w = 0.02):
        """


        Parameters
        ----------
        scheme : TYPE
            DESCRIPTION.
        sigma_w : TYPE, optional
            DESCRIPTION. The default is 0.02.

        Returns
        -------
        None.

        """
        super().__init__()
        self.scheme = scheme
        self.sigma_w = sigma_w

        # self.weightingM, self.binSelecteD, self.omegaM = self.calWeightingM()
        self.weightingM = self.calWeightingM()
        
    @property
    def scheme(self):
        return self.__scheme
    @scheme.setter
    def scheme(self, sh):
        self.__scheme = sh
    @property
    def weightingM(self):
        return self.__weightingM
    @weightingM.setter
    def weightingM(self, wM):
        self.__weightingM = wM
    @property
    def sigma_w(self):
        return self.__sigma_w
    @sigma_w.setter
    def sigma_w(self, sw):
        self.__sigma_w = sw

    def calWeightingM(self):
        linkS = self.scheme.linkS

        weightingM = []
        # binSelecteD = []
        # omegaM = []

        coordX = self.scheme.selection.coordX
        coordY = self.scheme.selection.coordY
        x_voxeL = np.array(coordX)
        y_voxeL = np.array(coordY)
        x_voxeL += self.scheme.vx_width/2
        y_voxeL += self.scheme.vx_length/2
        x_voxeL = x_voxeL[0:-1]
        y_voxeL = y_voxeL[0:-1]


        for l in range(len(linkS)):
            omegaR = self.scheme.selection.selecteD

            sigma_w = self.sigma_w
            d = linkS[l].calLinkDistance()

            for x in x_voxeL:
                idx_x = int(self.scheme.selection.getXIndex(x,
                                                            True))
                for y in y_voxeL:
                    idx_y = int(self.scheme.selection.getYIndex(y,
                                                                    True))
                    lambda_l = linkS[l].calDistanceFromNode((x,y)) - d
                    omegaR[idx_x][idx_y] = math.exp(-lambda_l/(2*sigma_w))

            weightingM.append(omegaR)
        wM = RTIWeightCalculator.transformWeightingM(weightingM)
        return wM #, binSelecteD, omegaM
    
    def getSetting(self):
        se = super().getSetting()
        se['WeightAlgorithm'] = 'ExpD'
        return se