# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 18:44:39 2021

@author: krong
"""

from rti_cal import RTIWeightCalculator
import numpy as np
import math

class LineWeightingRTICalculator(RTIWeightCalculator):
    def __init__(self, scheme, mode = 0):
        """


        Parameters
        ----------
        scheme : RTI Scheme
            DESCRIPTION.
            The object contains the inforamtion of setting and environments
        mode : Integer, optional
            DESCRIPTION. The default is 0.
            MODE 0 is the default mode the weight of the relation between
                pixel and radio link
            Alternative MODE. Divide by Square Root of Link Distance
        Returns
        -------
        None.

        """
        super().__init__()
        self.scheme = scheme
        self.mode = mode
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
    def mode(self):
        return self.__mode
    @mode.setter
    def mode(self, m):
        self.__mode = m

    def calWeightingM(self):
        linkS = self.scheme.linkS
        coordX = self.scheme.selection.coordX
        coordY = self.scheme.selection.coordY
        weightingM = []
        # binSelecteD = []
        # omegaM = []

        for l in range(len(linkS)):
            binaryR = self.scheme.selection.selecteD
            omegaR = self.scheme.selection.selecteD
            diff_x = linkS[l].getXDiff()
            diff_y = linkS[l].getYDiff()
            intersectionS = []
            if not diff_x == 0.:
                for i in range(len(coordX)):
                    rt, y, isInRange = linkS[l].getXRatio(coordX[i])
                    if isInRange:
                        intersectionS.append((coordX[i],
                                              y,
                                              rt))
            if not diff_y == 0.:
                for i in range(len(coordY)):
                    rt, x, isInRange = linkS[l].getYRatio(coordY[i])
                    if isInRange:
                        intersectionS.append((x,
                                              coordY[i],
                                              rt))
            intersectionS.sort(key = lambda intersectionS: intersectionS[0])
            for i in range(len(intersectionS)-1):
                x = intersectionS[i][0]
                y = intersectionS[i][1]
                d_rt = intersectionS[i+1][2] - intersectionS[i][2]
                w = d_rt * linkS[l].distance
                if self.mode:
                    w = w/math.sqrt(linkS[l].distance)
                try:
                    idx_x = int(self.scheme.selection.getXIndex(x, (diff_x >= 0)))
                    idx_y = int(self.scheme.selection.getYIndex(y, (diff_y >= 0)))
                except ValueError:
                    print(f'Intersection ({x:.2f},{y:.2f}) are out of defined area')
                    continue
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
        se['WeightAlgorithm'] = 'LS'
        return se