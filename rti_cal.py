# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 11:37:11 2020

@author: krong
"""
from abc import ABCMeta, abstractmethod
import numpy as np
from rti_grid import RTIGrid

class RTIWeightCalculator(metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    def scheme(self):
        raise NotImplementedError
    def weightingM(self):
        raise NotImplementedError

    @abstractmethod
    def calWeightingM(self):
        pass
    
    def getShape(self):
        return self.scheme.getShape()
    
    def getSetting(self):
        return self.scheme.getSetting()   

    def calIdealLinkAtten(self, vxAtten):
        linkAttenArr = np.matmul(self.weightingM, vxAtten)
        return linkAttenArr

    def transformWeightingM(wM_in):
        wM_out = []
        for i in range(len(wM_in)):
            wM_out.append(RTIGrid.reshapeVoxelM2Arr(wM_in[i]))

        return np.array(wM_out)











