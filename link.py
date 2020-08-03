# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 07:41:39 2020

@author: krong
"""
from geoutil import Position

class Sensor:
    def __init__(self, pos):
        """
        Parameters
        ----------
        pos : 2D Coordination Object
            Position of the sensor node
        """
        self.pos = pos
        
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
            
        self.distance = self.calLinkDistance()
        self.value = value
        
    def calLinkDistance(self):
        d = Position.calDistance(self.sensor1.pos, self.sensor2.pos)
        return  d
    
    def getPositions(self):
        return (self.sensor1.pos, self.sensor2.pos)
    
    def getXDistance(self):
        return abs(self.sensor2.pos.x - self.sensor1.pos.x)

    def getYDistance(self):
        return abs(self.sensor2.pos.y - self.sensor1.pos.y)
    
    def getXRatio(self, x):
        x1 = self.sensor1.pos.x
        x2 = self.sensor2.pos.x
        y1 = self.sensor1.pos.y
        y2 = self.sensor2.pos.y
        
        dx_t = x2 - x1
        dx = x - x1
        rt = dx/dx_t
        dy_t = y2 - y1
        dy = rt * dy_t
        y = y1 + dy
        return (rt, y, (0 <= rt <= 1))
    
    def getYRatio(self, y):
        x1 = self.sensor1.pos.x
        x2 = self.sensor2.pos.x
        y1 = self.sensor1.pos.y
        y2 = self.sensor2.pos.y
        
        dy_t = y2 - y1
        dy = y - y1
        rt = dy/dy_t
        dx_t = x2 - x1
        dx = rt * dx_t
        x = x1 + dx
        return (rt, x, (0 <= rt <= 1))