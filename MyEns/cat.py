# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 22:04:08 2018

@author: msh
"""

import astropy.units as U
import astropy.coordinates as coord

from astroquery.vizier import Vizier
from astroquery.simbad import Simbad

import subprocess as sp


from . import env
from . import astro



class query():
    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
        self.acal = astro.calc(verb=self.verb)
        self.otype = {'Star': 'star', '*': "other"}
        
    def gaia(self, ra_deg, dec_deg, rad_deg=0.0027, max_mag=20,
             max_coo_err=1, max_sources=1):
        """
        Retrieves data from gaia for given cooridnates
        
        @param ra_deg: Flux value
        @type ra_deg: float
        @param dec_deg: Flux Error Value
        @type dec_deg: float
        @param max_mag: Flux Error Value
        @type max_mag: float
        @param max_coo_err: Flux Error Value
        @type max_coo_err: float
        @param max_sources: Flux Error Value
        @type max_sources: float
        
        @return: list
        """
        try:
            vquery = Vizier(columns=['Source', 'RA_ICRS',
                                     'DE_ICRS', 'e_RA_ICRS',
                                     'e_DE_ICRS', 'phot_g_mean_mag',
                                     'pmRA', 'pmDE', 'e_pmRA', 'e_pmDE',
                                     'Epoch', 'Plx'], row_limit=max_sources)
        
            field = coord.SkyCoord(ra=ra_deg, dec=dec_deg, unit=(U.deg, U.deg), frame='icrs')
        
            return(vquery.query_region(field, width="{:f}d".format(rad_deg),
                                       catalog="I/337/gaia")[0])
        except Exception as e:
            self.eetc.print_if(e)
            
    def name(self, name):
        v = Vizier(columns=['NOMAD1', 'RAJ2000', 'DEJ2000', 'Bmag',
                                     'Vmag', 'Rmag'], row_limit=1)
        result = v.query_object(name, catalog=["NOMAD"])
        return(result)
            
    def nomad(self, ra, dec, radius=0.0027, min_mag=10,
              max_mag=20, max_sources=1):
        try:
            c = coord.SkyCoord(ra, dec, unit=(U.deg, U.deg), frame='icrs')
            r = radius * U.deg
    
            vquery = Vizier(columns=['NOMAD1', 'RAJ2000', 'DEJ2000', 'Bmag',
                                     'Vmag', 'Rmag'], row_limit=max_sources)
    
            result = vquery.query_region(c, radius=r, catalog="NOMAD")[0]
            
            return(result)
        except Exception as e:
            self.eetc.print_if(e)
            
    def usno(self, ra, dec, radius=0.0027, min_mag=10,
              max_mag=20, max_sources=1):
        try:
            c = coord.SkyCoord(ra, dec, unit=(U.deg, U.deg), frame='icrs')
            r = radius * U.deg
    
            vquery = Vizier(columns=['USNO', 'RAJ2000', 'DEJ2000', 'Bmag',
                                     'Rmag'], row_limit=max_sources)
    
            result = vquery.query_region(c, radius=r, catalog="USNO-A2.0")[0]
            
            return(result)
        except Exception as e:
            self.eetc.print_if(e)
    
    def get_otype(self, ra, dec, radius=0.002):
        try:
            customSimbad = Simbad()
            customSimbad.add_votable_fields('otype')
            c = coord.SkyCoord(ra, dec, unit=(U.deg, U.deg), frame='icrs')
            result = customSimbad.query_region(
                    c, radius='{0} degrees'.format(radius))[0]
            return(result["OTYPE"].decode("utf-8"))
        except Exception as e:
            pass
        
    def is_star(self, ra, dec, radius=0.002):
        try:
            otype = self.get_otype(ra, dec, radius=radius)
            return(otype.upper() == "STAR")
        except Exception as e:
            return(False)
            

class astrometrynet():
    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
        
    def solve(self, in_file, tmp):
        completed = sp.Popen(['solve-field', "--overwrite", "--no-plot",
                            "--dir", tmp, in_file])
        