# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 16:02:14 2020

@author: krong
"""
from abc import ABCMeta, abstractmethod
import numpy as np
from geoutil import RTIGrid, Position
from link import RTILink, Sensor

class Selection():
    def __init__(self, rtiGrid, selecteD, coordX, coordY):
        self.rtiGrid = rtiGrid
        self.selecteD = selecteD
        self.coordX = coordX
        self.coordY = coordY

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

class RTIScheme(metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    def rtiGrid(self):
        raise NotImplementedError
    def sensorS(self):
        raise NotImplementedError
    def linkS(self):
        raise NotImplementedError
    def voxelS(self):
        raise NotImplementedError
    def selection(self):
        raise NotImplementedError

    @abstractmethod
    def initLinks(self):
        pass
    @abstractmethod
    def initVoxels(self):
        pass
    @abstractmethod
    def initSensors(self):
        pass
    @abstractmethod
    def getVoxelScenario():
        pass

class SidePositionScheme(RTIScheme):
    def __init__(
            self,
            ref_pos= Position(0.,0.),
            area_width=6.,
            area_length=10.,
            vx_width=1.,
            vx_length=1.,
            n_sensor=20,
            wa_width=4.,
            wa_length=10.):

        """
        Constructor of SidePositionScheme Class: Evaluation of RTI scheme in which
        sensors are deployed in the sideline of the area of interest

        Parameters
        ----------
        ref_pos : 2D Position, optional
            Reference Position at the lower left corner. The default is (0.,0.).
        area_width : Float, optional
            The defined width space dimension. The default is 6..
        area_length : Float, optional
            The defined length space dimension. The default is 10..
        vx_width : Float, optional
            The width of Voxels The default is 1..
        vx_length : TYPE, optional
            The length of The default is 1..
        n_sensor : Even Integer, optional
            Total number of the deployed sensors on both side. The default is 20.
        wa_width : TYPE, optional
            DESCRIPTION. The default is 4..
        wa_length : TYPE, optional
            DESCRIPTION. The default is 10..

        Returns
        -------
        None.

        """

        super().__init__()

        self.vx_width = vx_width
        self.vx_length = vx_length
        self.area_width = area_width
        self.area_length = area_length
        self.n_sensor = n_sensor
        self.wa_width = wa_width
        self.wa_length = wa_length

        self.rtiGrid = RTIGrid(area_width,
                               area_length,
                               vx_width,
                               vx_length,
                               ref_pos)

        self.voxelS, self.selection = self.initVoxels()
        self.sensorS = self.initSensors()
        self.linkS = self.initLinks()

    @property
    def vx_width(self):
        return self.__vx_width
    @vx_width.setter
    def vx_width(self, w):
        if w > 0:
            self.__vx_width = w
        else:
            raise ValueError('Voxel width must be positive')

    @property
    def vx_length(self):
        return self.__vx_length
    @vx_length.setter
    def vx_length(self, l):
        if l > 0:
            self.__vx_length = l
        else:
            raise ValueError('Voxel length must be positive')

    @property
    def area_width(self):
        return self.__area_width
    @area_width.setter
    def area_width(self, w):
        if w < self.vx_width:
            raise ValueError('Area Width must be positive and \
                             more than voxel width')
        self.__area_width = w

    @property
    def area_length(self):
        return self.__area_length
    @area_length.setter
    def area_length(self, l):
        if l > self.vx_length:
            self.__area_length = l
        else:
            raise ValueError('Area length must be positive and \
                             more than voxel length')

    @property
    def wa_width(self):
        return self.__wa_width
    @wa_width.setter
    def wa_width(self, w):
        if self.vx_width <= w <= self.area_width:
            self.__wa_width = w
        else:
            raise ValueError('Working area width must be more than \
                             voxel width and less than area width')

    @property
    def wa_length(self):
        return self.__wa_length
    @wa_length.setter
    def wa_length(self, l):
        if self.vx_length <= l <= self.area_length:
            self.__wa_length = l
        else:
            raise ValueError('Working area length must be more than \
                             voxel length and less than area length')

    def initVoxels(self):
        # Create all voxels from the RTI grid (area of interest)
        voxelS = self.rtiGrid.initVoxels()
        # Define the working area
        # How many voxel is omitted around the area between sensor and the working area
        dx = self.area_width - self.wa_width
        if dx < 0:
            raise ValueError('Working area width must be smaller than \
                             the width of the area of interest')
        dy = self.area_length - self.wa_length
        if dy < 0:
            raise ValueError('Working area length must be smaller than \
                             the length of the area of interest')
        dnx = int(np.floor(np.floor(dx / self.vx_width)/2))
        dny = int(np.floor(np.floor(dy / self.vx_length)/2))

        coordX = []
        for i in range(len(voxelS)):
            coordX.append(voxelS[i][0].ref_pos.x)
        coordX.append(voxelS[len(voxelS)-1][0].ref_pos.x +
                      voxelS[len(voxelS)-1][0].width)
        coordY = []
        for i in range(len(voxelS[0])):
            coordY.append(voxelS[0][i].ref_pos.y)
        coordY.append(voxelS[0][len(voxelS[0])-1].ref_pos.y +
                      voxelS[0][len(voxelS[0])-1].length)

        bVoxeL = np.zeros((len(voxelS), len(voxelS[0])))
        while dnx > 0:
            dnx -= 1

            voxelS = np.delete(voxelS, dnx, 0)
            voxelS = np.delete(voxelS, -(dnx+1), 0)

            bVoxeL = np.delete(bVoxeL, dnx, 0)
            bVoxeL = np.delete(bVoxeL, -(dnx+1), 0)

            coordX.remove(coordX[dnx])
            coordX.remove(coordX[-(dnx+1)])
        while dny > 0:
            dny -= 1

            voxelS = np.delete(voxelS, dny, 1)
            voxelS = np.delete(voxelS, -(dny+1), 1)

            bVoxeL = np.delete(bVoxeL, dny, 1)
            bVoxeL = np.delete(bVoxeL, -(dny+1), 1)

            coordY.remove(coordY[dny])
            coordY.remove(coordY[-(dny+1)])

        coordX = tuple(coordX)
        coordY = tuple(coordY)
        bVoxeL = tuple(bVoxeL)
        selection = Selection(self.rtiGrid, bVoxeL, coordX, coordY)
        return voxelS, selection

    def initSensors(self):
        if not (self.n_sensor % 2) == 0:
            ValueError('In a side-position scheme, the total number of sensors \
                      must be even')

        s_distance = self.rtiGrid.y_span / (self.n_sensor/2)
        start = s_distance/2

        s_pos_y = np.linspace(start,
                              start + s_distance * (self.n_sensor/2-1),
                              int(self.n_sensor/2))
        leftSideSensorS = []
        rightSideSensorS = []
        for y in s_pos_y:
            leftSideSensorS.append(Sensor(Position(self.rtiGrid.min_x, y)))
            rightSideSensorS.append(Sensor(Position(self.rtiGrid.max_x, y)))

        sensorS = tuple([leftSideSensorS, rightSideSensorS])
        return sensorS

    def initLinks(self):
        # In the side position scheme, the leftside sensors and rightside sensors
        # are linked.
        leftSideSensorS = self.sensorS[0][:]
        rightSideSensorS = self.sensorS[1][:]

        linkS = []
        for s1 in leftSideSensorS:
            for s2 in rightSideSensorS:
                linkS.append(RTILink(s1, s2, 0.))
        linkS = tuple(linkS)

        return linkS

    def getVoxelScenario(self, x_range, y_range):
        if x_range[0] > x_range[1] or y_range[0] > y_range[1]:
            raise ValueError('input must be in form (min, max)')

        vxS = np.zeros(self.selection.getShape())

        xIdX = self.selection.getXIndexArr(x_range)
        yIdX = self.selection.getYIndexArr(y_range)

        vxS[xIdX[0]:(xIdX[1]+1), yIdX[0]:(yIdX[1]+1)] = 1
        return vxS

    def getRTIDim(self):
        return (len(self.linkS), self.voxelS())

    def getSetting(self):
        setting = {}
        setting['Width'] = self.wa_width
        setting['Length'] = self.wa_length
        setting['Sensor Distance'] = self.area_width
        setting['Sensor Count'] = int(self.n_sensor)
        setting['Voxel Width'] = self.vx_width

        return setting
