# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 18:44:39 2021

@author: krong
"""

from rti_cal import RTIWeightCalculator
import numpy as np
from rti_util import Position
import math

class InvAreaRTICalculator(RTIWeightCalculator):
    def __init__(self, scheme, lambda_min = 0.03):
        """


        Parameters
        ----------
        scheme : TYPE
            DESCRIPTION.
        lambda_min : TYPE, optional
            DESCRIPTION. The default is 0.03.

        Returns
        -------
        None.

        """
        super().__init__()
        self.scheme = scheme
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
    def lambda_min(self):
        return self.__lambda_min
    @lambda_min.setter
    def lambda_min(self, l_min):
        self.__lambda_min = l_min

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

            lambda_min = self.lambda_min
            d = linkS[l].calLinkDistance()

            for x in x_voxeL:
                for y in y_voxeL:
                    idx_x = int(self.scheme.selection.getXIndex(x,
                                                                    True))
                    idx_y = int(self.scheme.selection.getYIndex(y,
                                                                    True))
                    if idx_x < len(omegaR) and idx_y < len(omegaR):
                        lambda_l = linkS[l].calDistanceFromNode(Position(x,y)) - d
                        if lambda_l < lambda_min:
                            lambda_l = lambda_min
                        area = math.pi * (1/4) * d * math.sqrt(2*d*lambda_l)
                        omegaR[idx_x][idx_y] = 1/area

            weightingM.append(omegaR)
        wM = RTIWeightCalculator.transformWeightingM(weightingM)
        return wM #, binSelecteD, omegaM
    
    def getSetting(self):
        se = super().getSetting()
        se['WeightAlgorithm'] = 'InvA'
        return se