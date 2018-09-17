# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 19:55:39 2018

@author: msh
"""
from sep import Background, extract

from numpy import sort as nsort
from numpy import polyfit as pof
from numpy import log as nlog
from numpy import asarray as ar
from numpy import power
from numpy import flip, unique, arange, append, std, average, amin, amax

from scipy.stats import linregress


from math import pow as mpow, sqrt as msqrt

from astropy.table import Table

from . import env

class sex():
    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
        
    def find(self, data, t=True):
        bkg = Background(data)
        data_sub = data - bkg
        all_objects = ar(extract(data_sub, 1.5, err=bkg.globalrms))
        all_objects = all_objects[all_objects['flag'] == 0]
            
        if t:            
            return(Table(all_objects))
        else:
            return(all_objects)
            
    def extract_xy(self, src):
        try:
            return(Table([src['x'], src['y']]))
        except Exception as e:
            self.eetc.print_if(e)

class fit():
    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
                    
    def polinom(self, xs, ys, power=1):
        try:
            m, b = pof(xs, ys, deg=power)
            return(m, b)
        except Exception as e:
            self.eetc.print_if(e)
            
            
    def polinom_weighted(self, xs, ys, w, power=1):
        try:
            m, b = pof(xs, ys, w=w, deg=power)
            return(m, b)
        except Exception as e:
            self.eetc.print_if(e)
            
    def log(self, xs, ys, power=2):
        try:
            m, b = pof(xs, nlog(ys), power)
            return(m, b)
        except Exception as e:
            self.eetc.print_if(e)
            
    def polinom_value_generator(self, xs, cons):
        try:
            cons = flip(cons, 0)
            ys = []
            for i in xs:
                the_y = 0
                the_pow = -1
                for u in cons:
                    the_pow += 1
                    the_y += mpow(i, the_pow) * u
                ys.append(the_y)
            return(ar(ys))
        except Exception as e:
            self.eetc.print_if(e)
            
    def scipy_fit(self, x, y):
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        return(slope, intercept, mpow(r_value, 2))
        
class math():
    def __init__(self, verb=True):
        self.verb = verb
        
    def group_array(self, in_array, col):
        ret = []
        uniques = self.get_unique(in_array, col)
        if not uniques is None:
            for i in uniques:
                ln = []
                for u in in_array:
                    if u[col] == i:
                        ln.append(u)
                ret.append(ar(ln))

            return ar(ret)
    
    def get_unique_lines(self, in_array):
        search_col = unique(in_array, axis=0)
        return(search_col)
    
    def get_unique(self, in_array, col):
        search_col = in_array[:, col]
        return unique(search_col)
    
    def reshape(self, data, width=2045, height=2049, box=64):
        prev_x = 0
        prev_y = 0
        x_step = arange(0, width + box, box)[:-2]
        y_step = arange(0, height + box, box)[:-2]
        x_step = append(x_step, width)
        y_step = append(y_step, height)
        
        for x in x_step[1:]:
            for y in y_step[1:]:
                sub_data = data[data[:,0] > prev_x]
                sub_data = sub_data[sub_data[:,0] <= x]
                
                sub_data = sub_data[sub_data[:,1] > prev_y]
                sub_data = sub_data[sub_data[:,1] <= y]
                yield(sub_data)
                prev_y = y
            prev_x = x
            prev_y = 0
            
    def stdv(self, data):
        return(std(data))
        
    def stdv_w(self, data, w):
        ave = average(data, weights=w)
        variance = average(power((data - ave), 2), weights=w)
        return (msqrt(variance))
        
    def normalize(self, arr, fact=1):
        ret = (arr - amin(arr)) / (amax(arr) - amin(arr))
        return ret * fact
