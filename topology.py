# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 16:02:14 2020

@author: krong
"""
from geoutil import *


class Scheme():
    def __init__(self, sensorPosition, rtiGrid):
        """
        Parameters
        ----------
        sensorPosition : List of 2D Coordinations
            Position of the sensors
        rtiGrid : Object of Class RTIGrid
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.sensorPosition = sensorPosition
        self.rtiGrid = rtiGrid


class SidePositonScheme(Scheme):
    def __init__(
            self,
            ref_pos=(
                0.,
                0.),
            area_width=6.,
            area_height=10.,
            vx_width=1.,
            vx_height=1.,
            n_sensor=18,
            wa_width=4.,
            wa_height=10.):
        """
        Constructor of SidePositionScheme Class: Evaluation of RTI scheme in which sensors are deployed in the sideline of the area of interest

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
        self.vx_length = vx_length
        self.n_sensor = n_sensor
        self.dist_ss = dist_ss
