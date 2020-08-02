# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 07:25:15 2020

@author: krong

Class Definition
"""
from math import floor
                
class Voxel:
    def __init__(self, idx, width, height, ref_pos):
        """
        

        Parameters
        ----------
        idx : TYPE
            DESCRIPTION.
        width : TYPE
            DESCRIPTION.
        length : TYPE
            DESCRIPTION.
        ref_pos : TYPE
            DESCRIPTION.
        value : TYPE
            Value associated with attenuation

        Returns
        -------
        None.

        """
        self.idx = idx
        self.width = width
        self.height = height
        self.ref_pos = ref_pos
    
    def getLeftBound(self):
        return self.ref_pos.x
    
    def getRightBound(self):
        return self.ref_pos.x + self.width
    
    def getLowerBound(self):
        return self.ref_pos.y
    
    def getUpperBound(self):
        return self.ref_pos.y + self.height
    
    def getLowerLeftCorner(self):
        return [self.ref_pos.x, self.ref_pos.y]
    
    def getUpperLeftCorner(self):
        return [self.ref_pos.x, self.ref_pos.y + self.height]
    
    def getLowerRightCorner(self):
        return [self.ref_pos.x + self.width, self.ref_pos.y]
    
    def getUpperRightCorner(self):
        return [self.ref_pos.x + self.width, self.ref_pos.y + self.height]
    
    def getArea(self):
        return self.width * self.height
        
class VoxelField:
    def __init__(self, voxel_w, voxel_l, n_x, n_y, voxel_mat, ref_pos):
        self.voxels = voxel_w
        self.voxel_l = voxel_l
        self.n_x = n_x
        self.n_y = n_y
        self.voxel_mat = voxel_mat
        self.ref_pos = ref_pos
        
    def findVoxelIdx(self, x,y):
        col = floor((x - self.ref_pos.x)/self.voxel_w)
        row = floor((y - self.ref.pos.y)/self.voxel_l)
        idx = col * self.n_y + row
        return idx