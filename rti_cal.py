# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 11:37:11 2020

@author: krong
"""
from abc import ABCMeta, abstractmethod
import numpy as np
from geoutil import RTIGrid
import copy

class RTIWeightCalculator(metaclass=ABCMeta):
    def __init__(self):
        super().__init__()
    
    def weightingM(self):
        raise NotImplementedError
    
    @abstractmethod 
    def calWeightingM(self):
        pass
    
    def calIdealLinkAtten(self, vxAtten):
        wM = RTIWeightCalculator.transformWeightingM(self.weightingM)
        linkAttenArr = np.matmul(wM, vxAtten)
        return linkAttenArr
    
    def transformWeightingM(wM_in):
        wM_out = []
        for i in range(len(wM_in)):
            wM_out.append(RTIGrid.reshapeVoxelM2Arr(wM_in[i]))
        
        return np.array(wM_out)

    
class LineWeightingRTICalculator(RTIWeightCalculator):
    def __init__(self, scheme):
        super().__init__()
        self.scheme = scheme
        self.weightingM, self.binSelecteD, self.omegaM = self.calWeightingM()

        
    def calWeightingM(self):
        linkS = self.scheme.linkS
        coordX = self.scheme.selection.coordX
        coordY = self.scheme.selection.coordY
        weightingM = []
        binSelecteD = []
        omegaM = []
        
        for l in range(len(linkS)):
            binaryR = copy.deepcopy(self.scheme.selection.selecteD)
            omegaR = copy.deepcopy(self.scheme.selection.selecteD)
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
            
            binSelecteD.append(binaryR)
            omegaM.append(omegaR)
            weightingM.append(weightingR)
        return weightingM, binSelecteD, omegaM
                
                
                
                    
        
        
        
                    
    
    