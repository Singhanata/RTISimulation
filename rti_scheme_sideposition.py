# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 18:04:35 2021

@author: krong
"""

from rti_scheme import RTIScheme
from rti_util import Position, Sensor, RTILink
import numpy as np

class SidePositionScheme(RTIScheme):
    def __init__(
            self,
            ref_pos=(0.,0.),
            area_width=6.,
            area_length=10.,
            vx_width=1.,
            vx_length=1.,
            wa_width=4.,
            wa_length=10.,
            n_sensor=20):

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
        wa_width : TYPE, optional
            DESCRIPTION. The default is 4..
        wa_length : TYPE, optional
            DESCRIPTION. The default is 10..
        n_sensor : Even Integer, optional
            Total number of the deployed sensors on both side. The default is 20.
        Returns
        -------
        None.

        """

        super().__init__(ref_pos, 
                         area_width,
                         area_length,
                         vx_width,
                         vx_length,
                         wa_width,
                         wa_length,
                         n_sensor)

        self.sensorS = self.initSensors()
        self.linkS = self.initLinks()

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
            leftSideSensorS.append(Sensor((self.rtiGrid.min_x, y)))
            rightSideSensorS.append(Sensor((self.rtiGrid.max_x, y)))

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
        xrs = [s.pos[0] for s in self.sensorS[1]]
        yrs = [s.pos[1] for s in self.sensorS[1]]

        xs = xls + xrs
        ys = yls + yrs

        return [xs,ys]
    
    def getSetting(self):
        se = super().getSetting()
        se['scheme'] = 'SW'
        return se
    
    def describe(self):
        s = super().describe(self)
        s += '-Sideway_Poistioning'
        return s

    def show(self, **kw):
        super().show('side-scheme.svg', **kw);
