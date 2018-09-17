# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 19:55:39 2018

@author: msh
"""

from shutil import copy2, move
from os import remove
from os.path import isfile, exists, splitext, realpath, dirname, basename
from  numpy import genfromtxt, savetxt

from . import env

class op():
    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
        
    def cp(self, src, dst):
        try:
            self.eetc.print_if("Copying file {0} to {1}".format(src, dst))
            copy2(src, dst)
        except Exception as e:
            self.eetc.print_if(e)
            
    def mv(self, src, dst):
        try:
            self.eetc.print_if("Moving file {0} to {1}".format(src, dst))
            move(src, dst)
        except Exception as e:
            self.eetc.print_if(e)
            
    def rm(self, src):
        try:
            self.eetc.print_if("Removing file {0}".format(src))
            remove(src)
        except Exception as e:
            self.eetc.print_if(e)
            
    def is_file(self, src):
        try:
            self.eetc.print_if("Checking if file {0} exist".format(src))
            return(isfile(src))
        except Exception as e:
            self.eetc.print_if(e)
            return(False)
        
    def is_dir(self, src):
        try:
            self.eetc.print_if("Checking if directory {0} exist".format(src))
            return((not self.is_file(src)) and exists(src))
        except Exception as e:
            self.eetc.print_if(e)
            return(False)
        
        
    def read_array(self, src, dm=" ", dtype=float):
        try:
            return(genfromtxt(src, comments='#', delimiter=dm, dtype=dtype))
        except Exception as e:
            self.eetc.print_if(e)
            
    def write_array(self, file_name, src, dm=" ", h=""):
        try:
            savetxt(file_name, src, delimiter=dm, newline='\n', header=h)
        except Exception as e:
            self.eetc.print_if(e)
            
    def get_base_name(self, src):
        try:
            pn = dirname(realpath(src))
            fn = basename(realpath(src))
            return(pn, fn)
        except Exception as e:
            self.eetc.print_if(e)
    
    def get_extension(self, src):
        try:
            name = splitext(src)[0]
            extension = splitext(src)[1]
            return(name, extension)
        except Exception as e:
            self.fetc.print_if(e)
    
    def split_file_name(self, src):
        try:
            path, name = self.get_base_name(src)
            name , extension = self.get_extension(name)
            return(path, name, extension)
        except Exception as e:
            self.fetc.print_if(e)