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

class SidePositionScheme(RTIScheme):
    def __init__(
            self,
            ref_pos= Position(0.,0.),
            area_width=6.,
            area_height=10.,
            vx_width=1.,
            vx_height=1.,
            n_sensor=20,
            wa_width=4.,
            wa_height=10.):
        """
        Constructor of SidePositionScheme Class: Evaluation of RTI scheme in which
        sensors are deployed in the sideline of the area of interest

        Parameters
        ----------
        ref_pos : 2D Position, optional
            Reference Position at the lower left corner. The default is (0.,0.).
        area_width : Float, optional
            The defined width space dimension. The default is 6..
        area_height : Float, optional
            The defined height space dimension. The default is 10..
        vx_width : Float, optional
            The width of Voxels The default is 1..
        vx_height : TYPE, optional
            The height of The default is 1..
        n_sensor : Even Integer, optional
            Total number of the deployed sensors on both side. The default is 20.
        wa_width : TYPE, optional
            DESCRIPTION. The default is 4..
        wa_height : TYPE, optional
            DESCRIPTION. The default is 10..

        Returns
        -------
        None.

        """
        super().__init__()
        
        self.rtiGrid = RTIGrid(area_width,
                               area_height,
                               vx_width,
                               vx_height,
                               ref_pos)
        self.area_width = area_width
        self.area_height = area_height
        self.vx_width = vx_width
        self.vx_height = vx_height
        self.n_sensor = n_sensor
        self.wa_width = wa_width
        self.wa_height = wa_height

        self.voxelS, self.selection = self.initVoxels()
        self.sensorS = self.initSensors()
        self.linkS = self.initLinks()


    def initVoxels(self):
        # Create all voxels from the RTI grid (area of interest)
        voxelS = self.rtiGrid.initVoxels()
        # Define the working area
        # How many voxel is omitted around the area between sensor and the working area
        dx = self.area_width - self.wa_width
        if dx < 0:
            raise ValueError('Working area width must be smaller than the width \
                             of the area of interest')
        dy = self.area_height - self.wa_height
        if dy < 0:
            raise ValueError('Working area height must be smaller than the height \
                             of the area of interest')
        dnx = int(np.floor(np.floor(dx / self.vx_width)/2))
        dny = int(np.floor(np.floor(dy / self.vx_height)/2))
        
        coordX = []
        for i in range(len(voxelS)):
            coordX.append(voxelS[i][0].ref_pos.x)
        coordX.append(voxelS[len(voxelS)-1][0].ref_pos.x + 
                      voxelS[len(voxelS)-1][0].width)
        coordY = []
        for i in range(len(voxelS[0])):
            coordY.append(voxelS[0][i].ref_pos.y)
        coordY.append(voxelS[0][len(voxelS[0])-1].ref_pos.y + 
                      voxelS[0][len(voxelS[0])-1].height)
            
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
        if self.n_sensor % 2:
            TypeError('In a side-position scheme, the total number of sensors \
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
        
        x_min = x_range[0]
        x_max = x_range[1]
        y_min = y_range[0]
        y_max = y_range[1]
        
        for i in range(len(self.voxelS)):
            for j in range(len(self.voxelS[i])):
                pass
    
    def getRTIDim(self):
        return (len(self.linkS), self.voxelS())
