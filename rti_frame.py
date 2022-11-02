# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 09:23:57 2022

@author: krong
"""


class FrameIndex:
    TYPE = 0
    ID = 1
    sNID = 2
    sDID = 3
    LENGTH_START = 8
    MASK = 12
    PAYLOAD = 16
    
class FrameSymbol:
    BEACON = 0x00
    CONTENT = 0x01
    MASK = 255
    SIZE = 4