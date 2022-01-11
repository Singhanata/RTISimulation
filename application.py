# -*- coding: utf-8 -*-
"""
Created on Wed May 19 14:05:05 2021

@author: krong
"""
from rti_sim import RTISimulation
from rti_exp_position import process_position
from rti_exp_formfactor import process_formfactor
from rti_exp_alpha import process_alpha
from rti_exp_sensor import process_sensor
from rti_exp_voxel import process_voxel
from rti_exp_weightalgorithm import process_weightalgorithm
from rti_animation import process_animate

if __name__ == "__main__":
    rti = RTISimulation()
    process_animate(rti)
