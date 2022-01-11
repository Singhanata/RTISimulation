# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 15:15:26 2020

@author: krong
"""
import numpy as np
import sys
from rti_grid import RTIGrid

class RTIEstimator():
    def __init__(self, weightCalculator, alpha = 1.):
        self.weightCalculator = weightCalculator
        self.coeffM, self.weightingMT = self.initEstimator(alpha)

    @property
    def coeffM(self):
        return self.__coeffM
    @coeffM.setter
    def coeffM(self, cM):
        self.__coeffM = cM
    @property
    def weightingMT(self):
        return self.__weightingMT
    @weightingMT.setter
    def weightingMT(self, wMT):
        self.__weightingMT = wMT

    def initEstimator(self, alpha):
        weightingM = self.weightCalculator.weightingM
        weightingM_2 = RTIEstimator.calPower2M(weightingM)
        coeffM = weightingM_2

        if not alpha == 0:
            diffM = self.calDiffCoefficientM()
            coeffM += (alpha * diffM)
        else:
            if not np.linalg.cond(weightingM_2) < 1/sys.float_info.epsilon:
                raise Warning('weighting matrix product is singular, \
                              alpha must be more than 0')

        # coeffM_inv = np.linalg.inv(coeffM)
        # estimatorM = np.matmul(coeffM_inv, weightingM.transpose())

        return coeffM, weightingM.transpose()

    def calDiffCoefficientM(self):
        diffM_X, diffM_Y = RTIEstimator.buildDiffM(self.
                                                   weightCalculator.
                                                   getShape())
        diffM_X_2 = RTIEstimator.calPower2M(diffM_X)
        diffM_Y_2 = RTIEstimator.calPower2M(diffM_Y)

        return diffM_X_2 + diffM_Y_2

    def calVoxelAtten(self, linkAtten, normalized = False):
        try:
            bM = np.matmul(self.weightingMT, linkAtten)
            voxelAtten = np.linalg.solve(self.coeffM, bM)
            iM = (RTIGrid.reshapeVoxelArr2Im(voxelAtten, self.getShape()))
            if normalized:
                iM = iM/np.amax(iM)
            return iM
        except:
            raise ValueError(f'input must be array of link attenuation \
                  (length={self.estimatorM[1]}')

    def getShape(self):
        return self.weightCalculator.getShape()
    def buildDiffM(dim):
        x = dim[0]
        y = dim[1]

        r_dx = (x-1) * y
        r_dy = x * (y-1)
        c = x * y
        temp_DX = np.zeros((r_dx,c))
        temp_DY = np.zeros((r_dy,c))

        pos = 0
        for i in range(r_dx):
            temp_DX[i][pos] = -1
            temp_DX[i][pos+1] = 1
            pos += 1

            if i % (x-1) == (x-2):
                pos += 1

        diffM_X = np.array(temp_DX)

        pos = 0
        for i in range(r_dy):
            temp_DY[i][pos] = -1
            pos += x
            temp_DY[i][pos] = 1

            if i % (y-1) == (y-2):
                pos += (x+1)
                pos %= c

        diffM_Y = np.array(temp_DY)

        return diffM_X, diffM_Y

    def calPower2M(X):
        X = np.array(X)
        return np.matmul(X.transpose(), X)


