# -*- coding: utf-8 -*-
"""
Created on Wed May 19 14:05:05 2021

@author: krong
"""
from rti_sim import RTISimulation
from rti_exp_parameter import process_alpha

if __name__ == "__main__":
    rti = RTISimulation()
    process_alpha(rti)
