# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 18:16:25 2021

@author: krong
"""

from rti_scheme import RTIScheme
from rti_grid import RTIGrid
from rti_util import Sensor, RTILink
import numpy as np

class RectangularScheme(RTIScheme):
    def __init__(
            self,
            ref_pos=(0.,0.),
            area_width=10.,
            area_length=10.,
            vx_width=1.,
            vx_length=1.,
            wa_width=10.,
            wa_length=10.,
            n_sensor=20,
            ns_x=-1,
            ns_y=-1):

        """
        Constructor of SquareScheme Class:
        Evaluation of RTI scheme in which
        sensors are deployed in the borderline of a Rectangular
        with  equal distribution

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

        if area_length < area_width:
            raise ValueError('Width must be shorter than Length')

        self.n_sensor = n_sensor
        self._nx = ns_x
        self._ny = ns_y
        self.rtiGrid = RTIGrid(area_width,
                               area_length,
                               vx_width,
                               vx_length,
                               wa_width,
                               wa_length,
                               ref_pos)

        self.sensorS = self.initSensors()
        self.linkS = self.initLinks()

    @property
    def vx_width(self):
        return self.rtiGrid.gx_span
    @vx_width.setter
    def vx_width(self, w):
        if w > 0:
            self.rtiGrid.gx_span = w
        else:
            raise ValueError('Voxel width must be positive')

    @property
    def vx_length(self):
        return self.rtiGrid.gy_span
    @vx_length.setter
    def vx_length(self, l):
        if l > 0:
            self.rtiGrid.gy_span = l
        else:
            raise ValueError('Voxel length must be positive')

    @property
    def area_width(self):
        return self.rtiGrid.x_span
    @area_width.setter
    def area_width(self, w):
        if w < self.rtiGrid.gx_span:
            raise ValueError('Area Width must be positive and \
                             more than voxel width')
        self.rtiGrid.x_span = w

    @property
    def area_length(self):
        return self.rtiGrid.y_span
    @area_length.setter
    def area_length(self, l):
        if l > self.rtiGrid.gy_span:
            self.rtiGrid.y_span = l
        else:
            raise ValueError('Area length must be positive and \
                             more than voxel length')

    @property
    def wa_width(self):
        return self.rtiGrid.sx_span
    @wa_width.setter
    def wa_width(self, w):
        if self.rtiGrid.gx_span <= w <= self.rtiGrid.area_width:
            self.rtiGrid.sx_span = w
        else:
            raise ValueError('Working area width must be more than \
                             voxel width and less than area width')

    @property
    def wa_length(self):
        return self.rtiGrid.sy_span
    @wa_length.setter
    def wa_length(self, l):
        if self.rtiGrid.gy_span <= l <= self.rtiGrid.area_length:
            self.rtiGrid.sy_span = l
        else:
            raise ValueError('Working area length must be more than \
                             voxel length and less than area length')

    @property
    def selection(self):
        return self.rtiGrid.selectedGrid

    @property
    def coordX(self):
        return self.selection.coordX
    @property
    def coordY(self):
        return self.selection.coordY


    def initSensors(self):
        if not (self.n_sensor % 2) == 0:
            ValueError('In a recctangular scheme, the total number of sensors \
                      must be even')
        # จำนวนเซนเซอร์ของคู่ด้านกว้างและคู่ด้านยาวต้องเท่ากัน แสดงว่าผลรวมของจำนวนดังกล่าวจะต้องเท่ากับครึ่งหนึ่งของจำนวนเซนเซอร์
        # x+y=n/2 and x/y = x_span/y_span แก้ระบบสมการเพื่อหาจำนวนเซนเซอร์บนด้านทั้งสอง
        if (self._nx <= 1) or (self._ny <= 1):
            A = np.array([[1,1],[self.area_length, (-1) * self.area_width]])
            b = np.array([self.n_sensor/2, 0])
            ns = np.linalg.solve(A,b)
            # Check if the result is valid for furhter calculation
            if not (ns[0].is_integer() & ns[1].is_integer()):
                raise ValueError('The total number of sensor' + 
                                 ' cannot be arranged equally on each side')
            self._nx = ns[0]
            self._ny = ns[1]
        else:
            if not ((self._nx + self._ny)*2 == self.n_sensor):
                raise ValueError('The given sensor count is inconsistant')

        sx_distance = self.area_width / (self._nx)
        sy_distance = self.area_length / (self._ny)

        leftSideSensorS = []
        s_pos_y = np.arange(0.0, self.area_length, sy_distance)
        for pos_y in s_pos_y:
            leftSideSensorS.append(Sensor((0.0, pos_y)))

        topSideSensorS = []
        s_pos_x = np.arange(0.0, self.area_width, sx_distance)
        for pos_x in s_pos_x:
            topSideSensorS.append(Sensor((pos_x, self.area_length)))

        rightSideSensorS = []
        s_pos_y = np.arange(self.area_length, 0.0, (-1) * sy_distance)
        for pos_y in s_pos_y:
            rightSideSensorS.append(Sensor((self.area_width, pos_y)))

        bottomSideSensorS = []
        s_pos_x = np.arange(self.area_width, 0.0, (-1) * sx_distance)
        for pos_x in s_pos_x:
            bottomSideSensorS.append(Sensor((pos_x, 0.0)))

        sensorS = tuple([leftSideSensorS, topSideSensorS, rightSideSensorS, bottomSideSensorS])
        return sensorS


    def initLinks(self):
        # In the side position scheme, the leftside sensors and rightside sensors
        # are linked.
        leftSideSensorS = self.sensorS[0][:]
        topSideSensorS = self.sensorS[1][:]
        rightSideSensorS = self.sensorS[2][:]
        bottomSideSensorS = self.sensorS[3][:]

        linkS = []
        for s1 in leftSideSensorS:
            for s2 in topSideSensorS[1:]:
                linkS.append(RTILink(s1, s2, 0.))
            for s2 in rightSideSensorS:
                linkS.append(RTILink(s1, s2, 0.))

            if (s1.pos[1] == 0.0): continue
            for s2 in bottomSideSensorS:
                linkS.append(RTILink(s1, s2, 0.))

        for s1 in topSideSensorS:
            for s2 in rightSideSensorS[1:]:
                linkS.append(RTILink(s1, s2, 0.))
            for s2 in bottomSideSensorS:
                linkS.append(RTILink(s1, s2, 0.))

        for s1 in rightSideSensorS:
            for s2 in bottomSideSensorS[1:]:
                linkS.append(RTILink(s1, s2, 0.))

        linkS = tuple(linkS)
        return linkS

    def getSetting(self):
        se = super().getSetting()
        se['scheme'] = 'RE'
        return se

    def getSensorPosition(self):
        """
        Calculation of Sensor Positions for visualization

        Returns
        -------
        list of Sensor Positions
            DESCRIPTION.

        """
        xls = [s.pos[0] for s in self.sensorS[0]]
        yls = [s.pos[1] for s in self.sensorS[0]]
        xts = [s.pos[0] for s in self.sensorS[1]]
        yts = [s.pos[1] for s in self.sensorS[1]]
        xrs = [s.pos[0] for s in self.sensorS[2]]
        yrs = [s.pos[1] for s in self.sensorS[2]]
        xbs = [s.pos[0] for s in self.sensorS[3]]
        ybs = [s.pos[1] for s in self.sensorS[3]]

        xs = xls + xts + xrs + xbs
        ys = yls + yts + yrs + ybs

        return [xs,ys]

    def show(self, **kw):
        super().show('rect-scheme.svg', **kw);

