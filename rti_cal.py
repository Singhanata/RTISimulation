# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 11:37:11 2020

@author: krong
"""
from abc import ABCMeta, abstractmethod
from rti_scheme import Scheme, SidePositonScheme, Selection
import numpy as np

class RTICalculator(metaclass=ABCMeta):
    def __init__(self):
        super.__init__()
    
    def weightingM(self):
        raise NotImplementedError
    
    @abstractmethod 
    def calWeightingM(self):
        pass
    
class LineWeightingRTICalculator(RTICalculator):
    def __init__(self, scheme):
        if not isinstance(scheme, 'RTIScheme'):
            raise TypeError('scheme must be an instance of RTIScheme Class')
        self.scheme = scheme
        self.weightingM, self.binSelecteD, self.omegaM = self.calWeightingM()
        
    def calWeightingM(self):
        binaryM = self.scheme.selection.selecteD[:]
        omegaM = 1. * self.scheme.selection.selecteD[:]
        linkS = self.scheme.linkS
        coordX = self.scheme.selection.coordX
        coordY = self.scheme.selection.coordY
        
        for l in linkS:
            for _ in range(len(coordX)):
                rt, isInRange, y = l.getXRatio(coordX[_])
                if isInRange:
                    pass # TODO: End of the day at the calculation weightingM
            
    