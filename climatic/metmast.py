# -*- coding: utf-8 -*-
'''
MetMast
-------

A straightforward met mast import class built with the pandas library

'''
import pandas as pd

class MetMast(pd.DataFrame): 
    '''Subclass of the pandas dataframe built to import and quickly analyze
       met mast data.'''
       
    def __init__(self, lat=None, long=None, height=None, time_zone=None):
        '''Data structure with both relevant information about the mast
        itself (coordinates, height, time zone), as well as methods to process
        the met mast data and manipulate it using tools from the pandas
        library. 
        
        Parameters
        ----------
        lat: float, default None
            Latitude of met mast
        long: float, default None
            Longitude of met mast
        height: float or int, default None
            Height of met mast
        time_zone: string
            Please follow the pytz time zone conventions: 
            http://pytz.sourceforge.net/
        '''
        self.lat = lat
        self.long = long
        self.height = height
        self.time_zone = time_zone