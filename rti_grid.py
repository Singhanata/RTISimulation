# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 10:36:58 2021

@author: krong
"""
import numpy as np
import copy

class Selection():
    def __init__(self, coordX, coordY):
        self.coordX = coordX
        self.coordY = coordY

    @property
    def selecteD(self):
        return np.zeros(self.getShape())

    def getXIndex(self, x, isPositive):
        coordX = self.coordX
        if isPositive:
            for i in range(len(coordX)-1):
                if coordX[i] <= x < coordX[i+1]:
                    return i
            raise ValueError('input value is out of bound')
        else:
            for i in range(len(coordX)-1):
                if coordX[i+1] >= x > coordX[i]:
                    return i
            raise ValueError('input value is out of bound')

    def getYIndex(self, y, isPositive):
        coordY = self.coordY
        if isPositive:
            for i in range(len(coordY)-1):
                if coordY[i] <= y < coordY[i+1]:
                    return i
            raise ValueError('input value is out of bound')
        else:
            for i in range(len(coordY)-1):
                if coordY[i+1] >= y > coordY[i]:
                    return i
            raise ValueError('input value is out of bound')

    def getXIndexArr(self, x_range):
        try:
            min_x = x_range[0]
            max_x = x_range[1]
            if max_x < min_x:
                raise ValueError('input must have two value \
                                 in the ascending order')
        except:
            raise TypeError('input must be in form (min,max)')

        min_idx = self.getXIndex(min_x, True)
        max_idx = self.getXIndex(max_x, False)

        return (min_idx, max_idx)

    def getYIndexArr(self, y_range):
        try:
            min_y = y_range[0]
            max_y = y_range[1]
            if max_y < min_y:
                raise ValueError('input must have two value \
                                 in the ascending order')
        except:
            raise TypeError('input must be in form (min,max)')

        min_idx = self.getYIndex(min_y, True)
        max_idx = self.getYIndex(max_y, False)

        return (min_idx, max_idx)

    def getShape(self):
        return (len(self.coordX)-1,len(self.coordY)-1)

class RTIGrid:
    def __init__(self, x_span, y_span, gx_span, gy_span, sx_span, sy_span, ref_pos):
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
        sx_span : Float
            width of the selected area in x
        sy_span : Float
            width of the selected area in y
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
        self.sx_span = sx_span
        self.sy_span = sy_span

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
        self.selectedGrid = self.initSelectedVoxels()

    def getCoordination(self):
        return (self.coordX, self.coordY)

    def getVoxelMatrix(self):
        return np.zeros(self.nx, self.ny)

    def reshapeVoxelArr2Im(vArr, shape):
        vArr = np.array(vArr)
        im = vArr.reshape((shape[1],shape[0])).T
        return im

    def reshapeVoxelM2Arr(vM):
        vM = np.array(vM)
        return vM.transpose().reshape(-1).T

    def initSelectedVoxels(self):
        # How many voxel is omitted around the area between sensor and the working area
        dx = self.x_span - self.sx_span
        if dx < 0:
            raise ValueError('Working area width must be smaller than \
                             the width of the area of interest')
        dy = self.y_span - self.sy_span
        if dy < 0:
            raise ValueError('Working area length must be smaller than \
                             the length of the area of interest')
        dnx = int(np.floor(np.floor(dx / self.gx_span)/2))
        dny = int(np.floor(np.floor(dy / self.gy_span)/2))

        coordX = copy.deepcopy(self.coordX)
        coordY = copy.deepcopy(self.coordY)
        while dnx > 0:
            dnx -= 1

            coordX = np.delete(coordX, dnx)
            coordX = np.delete(coordX,-(dnx+1))
        while dny > 0:
            dny -= 1

            coordY = np.delete(coordY,dny)
            coordY = np.delete(coordY,-(dny+1))

        coordX = tuple(coordX)
        coordY = tuple(coordY)
        selection = Selection(coordX, coordY)

        return selection
