# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 07:41:39 2020

@author: krong
"""
from geoutil import Position

class RTILink:
    def __init__(self, sensor1, sensor2, value):
        """
        Parameters
        ----------
        sensor1 : TYPE
            DESCRIPTION.
        sensor2 : TYPE
            DESCRIPTION.
        value : TYPE
            Value associated with attenuation
        distance : 
            Distance of the link (btween S1 and S2)
        Returns
        -------
        None.
        """
        
        self.sensor1 = sensor1
        self.sensor2 = sensor2
        self.distance = self.calLinkDistance()
        self.value = value
        
    def calLinkDistance(self):
        d = Position.calDistance(self.sensor1.pos, self.sensor2.pos)
        return  d