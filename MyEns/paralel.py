# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 18:11:02 2018

@author: mshem
"""

from math import ceil
import threading

from . import env

class proc():
    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
        
    def job_devider(self, args, pieces=2):
        try:
            n = ceil(float(len(args))/float(pieces))
            for i in range(0, len(args), n):
                yield args[i:i + n]
        except Exception as e:
            self.eetc.print_if(e)
            
    def do_parallel(self, funck, args, pieces=2):
        try:
            splited_args = self.job_devider(args, pieces=pieces)
            lst = []
            for i in splited_args:
                lst.append(threading.Thread(target=funck, args=(i,)))
                
            for u in lst:
                u.start()
                
            for z in lst:
                z.join()
        except Exception as e:
            self.eetc.print_if(e)