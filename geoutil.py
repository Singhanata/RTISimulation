"""
Created on Thu Jul 30 07:35:20 2020

@author: krong
"""
from math import sqrt
import numpy as np
from voxel import Voxel

class Sensor:
    def __init__(self, pos):
        """
        Parameters
        ----------
        pos : 2D Coordination Object
            Position of the sensor node
        """
        self.pos = pos

class Position:
    """

    """
    def __init__(self, x, y):
        """
        Parameters
        ----------
        x : float
            x coordination
        y : float
            y coordination
        Returns
        -------
        None.

        """
        self.x = x
        self.y = y

    def calDistance(p1,p2):
        d = sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
        return d
class GridSquare():
    def __init__(self, ref_pos, x_span, y_span):
        """
        Parameters
        ----------
        ref_pos : 2D Coordination Object
            The object must have the 'x' and 'y' attribute
            Reference position on the lower left corner of the square
        x_span : float
            Width in x dimension
        y_span : float
            Width in y dimension

        Raises
        ------
        TypeError
             ref_pos must be 2D position with xy coordination
        """
        self.x_span = x_span
        self.y_span = y_span
        self.ref_pos = ref_pos
        self.area = x_span * y_span
        try:
            self.min_x = ref_pos.x
            self.min_y = ref_pos.y
            self.max_x = ref_pos.x + x_span
            self.max_y = ref_pos.y + y_span
        except:
            TypeError('ref_pos must have attributes "x" and "y"')

class RTIGrid:
    def __init__(self, x_span, y_span, gx_span, gy_span, ref_pos):
        """
        Parameters
        ----------
        x_span : Float
            width in x
        y_span : Float
            width in y
        gx_span : Float
            width of the unit grid square
        gy_span : Float
            width of the unit grid square
        ref_pos : 2D Position object
            Reference Position on the lower left corner

        Raises
        ------
        TypeError
            ref_pos must be 2D position with xy coordination
        """
        self.x_span = x_span
        self.y_span = y_span
        self.gx_span = gx_span
        self.gy_span = gy_span
        try:
            self.min_x = ref_pos.x
            self.min_y = ref_pos.y
            self.max_x = ref_pos.x + x_span
            self.max_y = ref_pos.y + y_span
        except:
            raise TypeError('The given position has no attribute "x" or "y"')
        self.nx = self.x_span/self.gx_span
        self.ny = self.y_span/self.gy_span

        self.coordX = np.linspace(self.min_x, self.max_x, int(self.nx + 1))
        self.coordY = np.linspace(self.min_y, self.max_y, int(self.ny + 1))

    def getCoordination(self):
        return (self.coordX, self.coordY)

    def initVoxels(self):
        ref_x = self.coordX[0:(len(self.coordX)-1)]
        ref_y = self.coordY[0:(len(self.coordY)-1)]

        voxelS = []
        for i in ref_x:
            for j in ref_y:
                voxelS.append(Voxel((i*self.nx + j),
                               self.gx_span,
                               self.gy_span,
                               Position(i,j)))
        voxelS = np.reshape(voxelS, (int(self.nx), int(self.ny)))

        return voxelS

# gr = RTIGrid(6.,10.,1.,1.,Position(0.,0.))
# V = gr.initVoxels()