# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 19:55:39 2018

@author: msh
"""

from datetime import datetime
import getpass
import platform

class etc():
    def __init__(self, verb=True):
        self.verb = verb
        
    def time_stamp(self):
        return(str(datetime.utcnow().strftime("%Y-%m-%IT%H:%M:%S")))
        
    def uname(self):
        return(str(getpass.getuser()))
        
    def system_info(self):
        si = platform.uname()
        return(("{0}{1}{2}{3}".format(si[0], si[2], si[5], self.uname())))
        
    def print_if(self, txt):
        if self.verb:
            print("{0}|{1}@{2}: {3}".format(
                    self.time_stamp(), self.uname(), self.system_info(), txt))