# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 16:02:14 2020

@author: krong
"""
from abc import ABCMeta, abstractmethod
import numpy as np
from geoutil import RTIGrid, Position, Sensor
from link import RTILink

class Selection():
    def __init__(self, rtiGrid, selecteD, coordX, coordY):
        self.rtiGrid = rtiGrid
        self.selecteD = selecteD
        self.coordX = coordX
        self.coordY = coordY

class RTIScheme(metaclass=ABCMeta):
    def __init__(self, rtiGrid):
        self.rtiGrid = rtiGrid
        super.__init__()

    def sensorS(self):
        raise NotImplementedError
    def linkS(self):
        raise NotImplementedError
    def voxelS(self):
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

class SidePositonScheme(RTIScheme):
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
            Total number of the deployed sensors on both side. The default is 18.
        wa_width : TYPE, optional
            DESCRIPTION. The default is 4..
        wa_height : TYPE, optional
            DESCRIPTION. The default is 10..

        Returns
        -------
        None.

        """
        self.area_width = area_width
        self.area_height = area_height
        self.vx_width = vx_width
        self.vx_height = vx_height
        self.n_sensor = n_sensor
        self.wa_width = wa_width
        self.wa_height = wa_height

        self.rtiGrid = RTIGrid(area_width,
                               area_height,
                               vx_width,
                               vx_height,
                               ref_pos)
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
        coordY = []
        for i in range(len(voxelS[0])):
            coordY.append(voxelS[0][i].ref_pos.y)
            
        bVoxeL = np.ones((len(voxelS), len(voxelS[0])))
        while dnx > 0:
            dnx -= 1
            bVoxeL[dnx][:] = 0
            bVoxeL[-(dnx+1)][:] = 0
            coordX.remove(coordX[dnx])
            coordX.remove(coordX[-(dnx+1)])
        while dny > 0:
            dny -= 1
            bVoxeL[:][dny] = False
            bVoxeL[:][-(dny+1)] = False
            coordY.remove(coordY[dny])
            coordY.remove(coordY[-(dny+1)])
        
        coordX = tuple(coordX)
        coordY = tuple(coordY)
        
        bVoxeL = tuple(bVoxeL > 0)
        
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
        for i in s_pos_y:
            leftSideSensorS.append(Sensor(Position(self.rtiGrid.min_x, i)))
            rightSideSensorS.append(Sensor(Position(self.rtiGrid.max_x, i)))

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
                linkS.append(RTILink(s1, s1, 0.))
        linkS = tuple(linkS)

sh = SidePositonScheme()