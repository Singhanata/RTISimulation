# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 16:02:14 2020

@author: krong
This class is an abstract class to normatize the interface between different
RTIScheme classes which defines the positions of sensors and links between
sensors
"""
import numpy as np
import matplotlib.pyplot as plt

from rti_grid import RTIGrid
from rti_util import Position, Sensor, RTILink

class RTIScheme():
    def __init__(self,
            ref_pos= Position(0.,0.),
            area_width=10.,
            area_length=10.,
            vx_width=1.,
            vx_length=1.,
            wa_width=10.,
            wa_length=10.,
            n_sensor=20):

        """
        Constructor of RTIScheme Class:

        Parameters
        ----------
        ref_pos : 2D Position, optional
            Reference Position at the lower left corner. The default is (0.,0.).
        area_width : Float, optional
            The defined width space dimension. The default is 10..
        area_length : Float, optional
            The defined length space dimension. The default is 10..
        vx_width : Float, optional
            The width of Voxels The default is 1..
        vx_length : TYPE, optional
            The length of The default is 1..
        wa_width : TYPE, optional
            DESCRIPTION. The default is 10..
        wa_length : TYPE, optional
            DESCRIPTION. The default is 10..
        n_sensor : Even Integer, optional
            Total number of the deployed sensors on both side. The default is 20.
        Returns
        -------
        None.

        """
        self.n_sensor = n_sensor
        self.rtiGrid = RTIGrid(area_width,
                               area_length,
                               vx_width,
                               vx_length,
                               wa_width,
                               wa_length,
                               ref_pos)

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

    @property
    def sensorS(self):
        return self.__sensorS
    @sensorS.setter
    def sensorS(self, sS):
        if any(isinstance(i, list) for i in sS):
            if (isinstance(sS[0][0], Sensor) ):
                self.__sensorS = sS
            else:
                raise ValueError('Not List of Sensor Type')
        else:
            if (isinstance(sS[0], Sensor) ):
                self.__sensorS = sS
            else:
                raise ValueError('Not List of Sensor Type')
    @property
    def linkS(self):
        return self.__linkS
    @linkS.setter
    def linkS(self, lS):
        if (isinstance(lS[0], RTILink)):
            self.__linkS = lS
        else:
            raise ValueError('Not List of Link Type')

    def initSensors(self):
        raise NotImplementedError
    def initLinks(self):
        raise NotImplementedError

    def getVoxelScenario(self, x_range, y_range):
        if x_range[0] > x_range[1] or y_range[0] > y_range[1]:
            raise ValueError('input must be in form (min, max)')

        vxS = np.zeros(self.selection.getShape())

        xIdX = self.selection.getXIndexArr(x_range)
        yIdX = self.selection.getYIndexArr(y_range)

        vxS[xIdX[0]:(xIdX[1]+1), yIdX[0]:(yIdX[1]+1)] = 1
        return vxS

    def getSetting(self):
        setting = {}
        setting['Width'] = self.wa_width
        setting['Length'] = self.wa_length
        setting['Sensor Distance'] = self.area_width
        setting['Sensor Count'] = int(self.n_sensor)
        setting['Voxel Width'] = self.vx_width
        return setting
    
    def describe(self):
        s = ('anchor@' + self.ref_pos.toString() + '-' +
             'area_dim@' + '(' + str(self.area_width) + ', ' + 
             str(self.area_length) + ')' + '-' +
             'voxel_dim@' + '(' + str(self.vx_width) + ', ' + 
             str(self.vx_length) + ')' + '-' +
             'N_sensor@' + str(self.n_sensor))
        return s
    def settingToCSV(self):
        s = ('anchor, ' + self.ref_pos.toString() + '\n' +
             'area_dim, ' + '(' + str(self.area_width) + ', ' + 
             str(self.area_length) + ')' + '\n' +
             'voxel_dim, ' + '(' + str(self.vx_width) + ', ' + 
             str(self.vx_length) + ')' + '\n' +
             'N_sensor, ' + str(self.n_sensor) + '\n')
        return s
    def getTitle(self):
        s = ('a@' + self.ref_pos.toString() + '-' +
             'dim@' + '(' + str(self.area_width) + ', ' + 
             str(self.area_length) + ')' + '-' +
             'vx@' + '(' + str(self.vx_width) + ', ' + 
             str(self.vx_length) + ')' + '-' +
             'N@' + str(self.n_sensor))
        return s

    def getShape(self):
        return self.selection.getShape()
    
    def getSensorPosition(self):
        raise NotImplementedError

    def show(self, fn = 'scheme.svg', **kw):
        sc = 'black'
        if 's_color' in kw:
            sc = kw['s_color']
        ss = 800
        if 's_size' in kw:
            ss = kw['s_size']
        sm = '.'
        if 's_marker' in kw:
            sm = kw['s_marker']
        lc = 'b'
        if 'l_color' in kw:
            lc = kw['l_color']

        fn = 'results/' + fn
        spos = self.getSensorPosition()
        linkS = self.linkS

        x_span = self.area_width
        y_span = self.area_length

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # Major ticks every 20, minor ticks every 5
        major_ticks = np.arange(0, x_span + 1, x_span/10)
        minor_ticks = np.arange(0, y_span + 1, y_span/50)

        plt.scatter(spos[0],
                spos[1],
                s=ss,
                c=sc,
                marker=sm)
        for l in linkS:
            (plt.plot([l.tx.pos.x, l.rx.pos.x],
                      [l.tx.pos.y, l.rx.pos.y],
                      '--',
                      color = lc,
                      linewidth = 1))
        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)
        ax.set_yticks(major_ticks)
        ax.set_yticks(minor_ticks, minor=True)

        ax.set_xlabel('X(m)')
        ax.set_ylabel('Y(m)')

        # Or if you want different settings for the grids:
        ax.grid(which='major', alpha=0.5, linewidth = 1, color='black')
        ax.grid(which='minor', alpha=0.2, linewidth = 0.5, color='black')

        ax.set_xlim(-x_span/10, x_span * 1.1)
        ax.set_ylim(-y_span/10, y_span * 1.1)

        plt.minorticks_on()

        plt.savefig(fn)
        plt.show()

