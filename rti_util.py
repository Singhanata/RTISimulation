"""
Created on Thu Jul 30 07:35:20 2020

@author: krong
"""
from math import sqrt

class Position:
    def calDistance(p1,p2):
        d = sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        return d
    
    def toString(obj):
        s = '(' + str(obj[0]) + ', ' + str(obj[1]) + ')'
        return s

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

    def calDistanceFromNode(self, pos):
        return Position.calDistance(pos, self.tx.pos) + Position.calDistance(
            pos, self.rx.pos)

    def getPositions(self):
        return (self.tx.pos, self.rx.pos)

    def getXDiff(self):
        return self.rx.pos[0] - self.tx.pos[0]

    def getYDiff(self):
        return self.rx.pos[1] - self.tx.pos[1]

    def getXRange(self):
        return [min(self.tx.pos[0], self.rx.pos[0]),
                    max(self.tx.pos[0], self.rx.pos[0])]

    def getYRange(self):
        return [min(self.tx.pos[1], self.rx.pos[1]),
                    max(self.tx.pos[1], self.rx.pos[1])]

    def getXRatio(self, x):
        x1 = self.tx.pos[0]
        x2 = self.rx.pos[0]
        y1 = self.tx.pos[1]
        y2 = self.rx.pos[1]

        dx_t = x2 - x1
        dx = x - x1
        rt = dx/dx_t
        dy_t = y2 - y1
        dy = rt * dy_t
        y = y1 + dy
        return (rt, y, (0 <= rt <= 1))

    def getYRatio(self, y):
        x1 = self.tx.pos[0]
        x2 = self.rx.pos[0]
        y1 = self.tx.pos[1]
        y2 = self.rx.pos[1]

        dy_t = y2 - y1
        dy = y - y1
        rt = dy/dy_t
        dx_t = x2 - x1
        dx = rt * dx_t
        x = x1 + dx
        return (rt, x, (0 <= rt <= 1))
