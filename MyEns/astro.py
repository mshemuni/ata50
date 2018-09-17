# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 19:55:39 2018

@author: msh
"""

from sep import Background, sum_circle

from astropy.io import fits as fts
from astropy.table import Table
from astropy import coordinates
from astropy import units as U
from astropy.time import Time

import subprocess as sp

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Ellipse
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib import cm

from math import pow as mpow
from math import sqrt as msqrt

import numpy as np

from . import env

class fits():
    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
        
    def header(self, src, field="*"):
        """
        Returns all or specified header and its value
        
        @param src: Source File Path.
        @type src: str
        @param field: Header Cart (Optional)
        @type field: str
        
        @return: list
        """
        ret = []
        try:
            hdu = fts.open(src, mode='readonly')
            for i in hdu[0].header:
                ret.append([i, hdu[0].header[i]])
                
            if field == "*":
                return(ret)
            else:
                return([field, hdu[0].header[field]])
        except Exception as e:
            self.eetc.print_if(e)
            
    def data(self, src, t=True):
        """
        Returns data of fit type file
        
        @param src: Source File Path.
        @type src: str
        @param t: Table return (Optional)
        @type t: boolean
        
        @return: numpy.ndarray or astropy.Table
        """
        try:
            hdu = fts.open(src, mode='readonly')
            data = hdu[0].data
            data = data.astype(np.float64)
            #data = data.byteswap().newbyteorder()
            if t:                
                return(Table(data))
            else:
                
                return(data)
        except Exception as e:
            self.eetc.print_if(e)
            
class calc():
    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
        
    def flux2magmerr(self, flux, fluxerr):
        """
        Calculates magnitudes from flux value
        
        @param flux: Flux value
        @type flux: float
        @param fluxerr: Flux Error Value
        @type fluxerr: float
        
        @return: list
        """
        try:
            mag, magerr = -2.5 * np.log10(flux), 2.5/np.log(10.0)*fluxerr/flux
            return(mag, magerr)
        except Exception as e:
            self.eetc.print_if(e)

    def radec2wcs(self, ra, dec):
        """
        Converts ra and dec values to coordinate
        
        @param ra: right ascension
        @type ra: float
        @param dec: Declination
        @type dec: float
        
        @return: coordinates.SkyCoord
        """
        try:
            c = coordinates.SkyCoord('{0} {1}'.format(ra, dec),
                                     unit=(U.hourangle, U.deg), frame='icrs')
            return(c)
        except Exception as e:
            self.eetc.print_if(e)
            
    def xy2sky(self, src, x, y):
        """
        Returns ra and dec values of a given x and y coordinates
        
        @param src: Source File Path
        @type src: str
        @param x: X Coordinate
        @type x: float
        @param y: Y Coordinate
        @type y: float
        
        @return: coordinates.SkyCoord
        """
        try:
            process = sp.Popen(['xy2sky', '-d', src,
                                str(x), str(y)], stdout=sp.PIPE)
            out, err = process.communicate()
            out = out.decode("utf-8").split()
           
            return(out[0], out[1])
        except Exception as e:
             self.eetc.print_if(e)
             
    def is_close_arc(self, coor1, coor2, max_dist=10):
        """
        Checks if two sky coordinates are within given distance
        
        @param coor1: First Coordinate
        @type coor1: list
        @param coor2: Second Coordinate
        @type coor2: list
        @param max_dist: Distance
        @type max_dist: float
        
        @return: boolean
        """
        try:
            c1 = self.radec2wcs(coor1[0], coor1[1])
            c2 = self.radec2wcs(coor2[0], coor2[1])
            
            ret = c1.separation(c2)
            return(ret.arcsecond < max_dist)
        except Exception as e:
            self.eetc.print_if(e)
        
    def is_close_phy(self, coor1, coor2, max_dist=15):
        """
        Checks if two physical coordinates are within given distance
        
        @param coor1: First Coordinate
        @type coor1: list
        @param coor2: Second Coordinate
        @type coor2: list
        @param max_dist: Distance
        @type max_dist: float
        
        @return: boolean
        """
        dX = coor1[0] - coor2[0]
        dY = coor1[1] - coor2[1]
        dist = msqrt(mpow(dX, 2) + mpow(dY, 2))
        return(dist < max_dist)

class time():
    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
        
    def jd(self, timestamp):
        """
        Calculates JD
        
        @param timestamp: Timestamp
        @type timestamp: str
        
        @return: float
        """
        if "T" not in timestamp:
            timestamp = str(timestamp).replace(" ", "T")
        
        t_jd = Time(timestamp, format='isot', scale='utc')

        return(t_jd.jd)
        
    def mjd(self, timestamp):
        """
        Calculates JD
        
        @param timestamp: Timestamp
        @type timestamp: str
        
        @return: float
        """
        if "T" not in timestamp:
            timestamp = str(timestamp).replace(" ", "T")
        
        t_jd = Time(timestamp, format='isot', scale='utc')

        return(t_jd.mjd)

class visual():
    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
        
    def plot_scatter_error(self, X, Y, error):
        fig, ax = plt.subplots()
        ax.errorbar(X, Y, yerr=error)
        plt.show()
        
    def plot_scatter(self, X, Y, x_label="Awesome Numbers", y_label="Awesome Numbers", title="Awesome Graph"):
        """
        Plots a 2D scatter graph of given xs and ys
        
        @param X: X points
        @type X: list
        @param Y: Y points
        @type Y: list
        @param x_label: X axis label
        @type x_label: str
        @param y_label: Y axis label
        @type y_label: str
        @param title: Graph title
        @type title: str
        
        @return: None
        """
        plt.clf()
        plt.plot(X, Y, "ro")
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.show()
        
    def plot_scatter_save(self, X, Y, out_file, x_label="Awesome Numbers", y_label="Awesome Numbers", title="Awesome Graph"):
        """
        Plots a 2D scatter graph of given xs and ys
        
        @param X: X points
        @type X: list
        @param Y: Y points
        @type Y: list
        @param x_label: X axis label
        @type x_label: str
        @param y_label: Y axis label
        @type y_label: str
        @param title: Graph title
        @type title: str
        
        @return: None
        """
        plt.clf()
        plt.plot(X, Y, "ro")
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.savefig(out_file)

    def plot_scatter2_save(self, X, Y1, Y2, out_file, t1="rx", t2="b+", x_label="Awesome Numbers", y_label="Awesome Numbers", title="Awesome Graph"):
        """
        Plots two 2D scatters graph of given xs and ys
        Usually used for plotting values and fit together
        
        @param X: X points
        @type X: list
        @param Y1: Y1 points
        @type Y1: list
        @param Y2: Y2 points
        @type Y2: list
        @param x_label: X axis label
        @type x_label: str
        @param y_label: Y axis label
        @type y_label: str
        @param title: Graph title
        @type title: str
        
        @return: None
        """
        plt.clf()
        plt.plot(X, Y1, t1)
        plt.plot(X, Y2, t2)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.savefig(out_file)

    def plot_scatter2(self, X, Y1, Y2, t1="rx", t2="b+", x_label="Awesome Numbers", y_label="Awesome Numbers", title="Awesome Graph"):
        """
        Plots two 2D scatters graph of given xs and ys
        Usually used for plotting values and fit together
        
        @param X: X points
        @type X: list
        @param Y1: Y1 points
        @type Y1: list
        @param Y2: Y2 points
        @type Y2: list
        @param x_label: X axis label
        @type x_label: str
        @param y_label: Y axis label
        @type y_label: str
        @param title: Graph title
        @type title: str
        
        @return: None
        """
        plt.clf()
        plt.plot(X, Y1, t1)
        plt.plot(X, Y2, t2)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.suptitle(title, fontsize=14, fontweight='bold')
        #plt.xlim(5, 0)
        plt.show()
        
    def plot(self, data, cmap="gray"):
        """
        Displays fits type file as whole
        
        @param data: Data of fits type file
        @type data: numpy.ndarray
        @param cmap: Color map
        @type cmap: str
        
        @return: None
        """
        try:
            rcParams['figure.figsize'] = [10., 8.]
            fig, ax = plt.subplots()
            m, s = np.mean(data), np.std(data)
            ax.imshow(data, interpolation='nearest', cmap=cmap,
                      vmin=m - s, vmax=m + s, origin='lower')
            plt.show()
        except Exception as e:
            self.eetc.print_if(e)
        
    def plot_sources(self, data, src, mark_color="red", cmap="gray"):
        """
        Displays fits type file and shows regions
        
        @param data: Data of fits type file
        @type data: numpy.ndarray
        @param src: List of X and Y coordinates of sources
        @type src: numpy.ndarray
        @param mark_color: Color of mark
        @type mark_color: str
        @param cmap: Color map
        @type cmap: str
        
        @return: None
        """
        try:
            rcParams['figure.figsize'] = [10., 8.]
            fig, ax = plt.subplots()
            m, s = np.mean(data), np.std(data)
            ax.imshow(data, interpolation='nearest', cmap=cmap,
                      vmin=m - s, vmax=m + s, origin='lower')
            
            for i in range(len(src)):
                e = Ellipse(xy=(src[i][0], src[i][1]),
                            width = 15,
                            height = 15)
                
                e.set_facecolor('none')
                e.set_edgecolor(mark_color)
                ax.add_artist(e)
            
            plt.show()
        except Exception as e:
            self.eetc.print_if(e)
        
    def plot_star(self, data, x, y, cmap="gray", offset=250):
        """
        Displays specified area of a fits type file
        
        @param data: Data of fits type file
        @type data: numpy.ndarray
        @param x: X Coordinate
        @type x: float
        @param y: Y coordinate
        @type y: float
        @param cmap: Color map
        @type cmap: str
        @param offset: width and height of desired area
        @type offset: float
        
        @return: None
        """
        try:
            tmp = x
            x = y
            y = tmp
            
            f_w, f_h = data.shape
            
            use_r = int(x + offset / 2)
            if f_w < int(x + offset / 2):
                use_r = f_w
            
            use_l = int(x - offset / 2)
            if int(x - offset / 2) < 0:
                use_l = 0
                
            use_t = int(y - offset / 2)
            if int(y - offset / 2) < 0:
                use_t = 0
            
            use_b = int(y + offset / 2)
            if f_h < int(y + offset / 2):
                use_b = f_h
            
            sub_data = data[use_l:use_r, use_t:use_b]
            
            
            
            h, w = sub_data.shape
            
            X = sub_data[:, int(h/2)]
            Y = sub_data[int(w/2), :]
            
            
            new_y = np.linspace(1, offset, num=offset)
            the_max = np.amax(sub_data)
            
            asp = offset / (the_max * 2)
            
            
            fig = plt.figure()
            ax1 = fig.add_subplot(2, 2, 1)
            ax2 = fig.add_subplot(2, 2, 3,
                                  adjustable='box', aspect=asp)
            ax3 = fig.add_subplot(2, 2, 2,
                                  adjustable='box', aspect=np.power(asp, -1))
            #ax2.set_ylim(min_val, max_val)
            #ax3.set_xlim(min_val, max_val)
            bounds = [0,w,0,h]
            ax1.imshow(sub_data, cmap='gray', extent=bounds, origin='lower')
            ax2.plot(Y, 'b-')
            ax3.plot(X, new_y, 'b-')
            plt.tight_layout()
            plt.subplots_adjust(hspace=0.001)
            plt.show()
        except Exception as e:
            self.eetc.print_if(e)
            
class phot():
    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
        self.calc = calc(verb=self.verb)
        
    def do(self, data, x_coor, y_coor, aper_radius=15.0, gain=1.21):
        """
        Do photometry of given coordinates
        
        @param data: Data of fits type file
        @type data: numpy.ndarray
        @param x_coor: X Coordinate
        @type x_coor: float
        @param y_coor: Y coordinate
        @type y_coor: float
        @param aper_radius: Radius of aperture for photometry
        @type aper_radius: float
        @param gain: Gain value of CCD chip
        @type gain: float
        
        @return: list
        """
        try:
            bkg = Background(data)
            data_sub = data - bkg
            flux, fluxerr, flag = sum_circle(data_sub, x_coor, y_coor,
                                             aper_radius, err=bkg.globalrms,
                                             gain=gain)
            return(flux, fluxerr, flag)
        except Exception as e:
            self.eetc.print_if(e)
