# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 18:44:39 2021

@author: krong
"""

from rti_cal import RTIWeightCalculator
import numpy as np
from rti_util import Position
import math

class EllipseRTICalculator(RTIWeightCalculator):
    def __init__(self, scheme, mode = 0, lambda_coeff = 0.03):
        """

        Parameters
        ----------
        scheme : RTI Scheme
            DESCRIPTION.
            The object contains the inforamtion of setting and environments
        mode : Integer, optional
            DESCRIPTION. The default is 0.
            MODE 0 lambda is static default at 0.03
                (Typical Value 0.03 - 0.003 for distance around 10 m)
            MODE 1 lambda varies with the voxel dimension
            MODe 2 lambda varies with the link distance
            Alternative MODE. -
        Returns
        -------
        None.

        """
        super().__init__()
        self.scheme = scheme
        self.mode = mode

        if (mode == 0):
            self.lambda_e = lambda_coeff
        elif (mode == 1):
            self.lambda_e = lambda_coeff * self.scheme.vx_width
        elif(mode == 2):
            self.lambda_e = lambda_coeff
        else:
            ValueError('Mode Not Defined')

        # self.weightingM, self.binSelecteD, self.omegaM = self.calWeightingM()
        self.weightingM = self.calWeightingM()

    @property
    def scheme(self):
        return self.__scheme;
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
    def lambda_e(self):
        return self.__lambda_e
    @lambda_e.setter
    def lambda_e(self, l_e):
        self.__lambda_e = l_e
    @property
    def mode(self):
        return self.__mode
    @mode.setter
    def mode(self, m):
        self.__mode = m

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
            binaryR = self.scheme.selection.selecteD
            omegaR = self.scheme.selection.selecteD

            x_range = linkS[l].getXRange()
            y_range = linkS[l].getYRange()
            # TODO: find the ellipse weighting algorithm

            lambda_e = self.lambda_e
            d = linkS[l].calLinkDistance()
            w = 1/math.sqrt(d)
            if (self.mode == 2):
                lambda_e = (d/10) * lambda_e
            # Boundary of voxel
            x_range[0] -= lambda_e * 2
            x_range[1] += lambda_e * 2
            y_range[0] -= lambda_e * 2
            y_range[1] += lambda_e * 2

            x_voxeL_l = x_voxeL[x_voxeL >= x_range[0]]
            x_voxeL_l = x_voxeL[x_voxeL <= x_range[1]]
            y_voxeL_l = y_voxeL[y_voxeL >= y_range[0]]
            y_voxeL_l = y_voxeL[y_voxeL <= y_range[1]]

            for x in x_voxeL_l:
                idx_x = int(self.scheme.selection.getXIndex(x,
                                                            True))
                for y in y_voxeL_l:
                    if(linkS[l].calDistanceFromNode((x,y)) <= d + lambda_e):
                        idx_y = int(self.scheme.selection.getYIndex(y,
                                                                    True))
                        if idx_x < len(binaryR) and idx_y < len(binaryR[0]):
                            binaryR[idx_x][idx_y] = 1.
                            omegaR[idx_x][idx_y] = w

            weightingR = np.multiply(binaryR, omegaR)

            # binSelecteD.append(binaryR)
            # omegaM.append(omegaR)
            weightingM.append(weightingR)
        wM = RTIWeightCalculator.transformWeightingM(weightingM)
        return wM #, binSelecteD, omegaM
    
    def getSetting(self):
        se = super().getSetting()
        se['WeightAlgorithm'] = 'EL'
        return se