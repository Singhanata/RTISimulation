"""
Created on Fri Sep 30 10:51:00 2022

@author: krong
"""
import os
from datetime import datetime

import threading

class ReceiveThread(threading.Thread):
    def __init__(self, threadID, name, counter, rtiConn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.rtiConn = rtiConn
    def run(self):
        print("Starting " + self.name)
        self.rtiConn.receive()
        print("Exiting " + self.name)

