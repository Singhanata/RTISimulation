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
    def __init__(self, tx, rx, value):
        """
        Parameters
        ----------
        tx : TYPE
            DESCRIPTION.
        rx : TYPE
            DESCRIPTION.
        value : TYPE
            Value associated with attenuation
        distance : 
            Distance of the link (btween S1 and S2)
        Returns
        -------
        None.
        """
        self.tx = tx
        self.rx = rx
        self.value = value
        self.distance = self.calLinkDistance()
        
    def calLinkDistance(self):
        d = Position.calDistance(self.tx.pos, self.rx.pos)
        return  d
    
    def getPositions(self):
        return (self.tx.pos, self.rx.pos)
    
    def getXDiff(self):
        return self.rx.pos.x - self.tx.pos.x

    def getYDiff(self):
        return self.rx.pos.y - self.tx.pos.y
    
    def getXRatio(self, x):
        x1 = self.tx.pos.x
        x2 = self.rx.pos.x
        y1 = self.tx.pos.y
        y2 = self.rx.pos.y
        
        dx_t = x2 - x1
        dx = x - x1
        rt = dx/dx_t
        dy_t = y2 - y1
        dy = rt * dy_t
        y = y1 + dy
        return (rt, y, (0 <= rt <= 1))
    
    def getYRatio(self, y):
        x1 = self.tx.pos.x
        x2 = self.rx.pos.x
        y1 = self.tx.pos.y
        y2 = self.rx.pos.y
        
        dy_t = y2 - y1
        dy = y - y1
        rt = dy/dy_t
        dx_t = x2 - x1
        dx = rt * dx_t
        x = x1 + dx
        return (rt, x, (0 <= rt <= 1))