# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 20:00:07 2022

@author: krong
"""
import numpy as np
import os
# import warning
from datetime import datetime

class RTIInput():
    def __init__(self, sz, dim, savepath, *args):
        self.log = {}
        self.prior = {}
        self.count = {}
        self.size = sz
        self.savepath = savepath
        self.ready = False
        for ar in args:
            self.log[ar] = {}
            self.prior[ar] = {}
            for i in range(dim[0]):
                self.log[ar][i+1] = np.zeros([dim[1], sz])
                self.prior[ar][i+1] = np.zeros([dim[1], 2])
            self.count[ar] = np.zeros(dim[0], dtype=int)
    
    def update(self, vl, key, sDID, idx):
        self.log[key][sDID][idx][self.input.count['rssi'][sDID-1]] = vl
        self.input
        if self.count[key] >= self.size:
            if not self.ready:
                self.prior[key][sDID][idx][0] = np.average(self.log[key][sDID][idx]
                                                           [self.input
                                                            .count['rssi'][sDID-1]])
            self.ready = True
            self.timeStr = datetime.now().strftime('_%d%m%Y_%H%M%S')
            filename = key + ' N' + str(sDID) + self.timeStr + '.csv'
            filepath = os.sep.join([self.savepath['rec'], filename])
            np.savetxt(filepath, self.log[key][sDID], 
                       delimiter = ',', fmt = '%s')


