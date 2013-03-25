# -*- coding: utf-8 -*-
'''
MetMast
-------

A straightforward met mast import and analysis class built
with the pandas library

'''
from __future__ import print_function
from __future__ import division
import os
import re
import pickle
import warnings
import pandas as pd
import numpy as np
import scipy.stats as spystats
from header_classifier import features
import weibull_est as west
import plottools


class MetMast(object):
    '''Subclass of the pandas dataframe built to import and quickly analyze
       met mast data.'''

    def __init__(self, lat=None, lon=None, height=None, time_zone=None):
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
        self.lon = lon
        self.height = height
        self.time_zone = time_zone
        
    def __repr__(self):
        if self.time_zone:
            zone_or_none = "'{0}'".format(self.time_zone)
        else:
            zone_or_none = None
        return ("climatic.MetMast(lat={0}, lon={1}, height={2}, " 
                "time_zone={3})").format(self.lat, 
                                         self.lon, 
                                         self.height, 
                                         zone_or_none)

    def wind_import(self, path, columns=None, header_row=None, time_col=None,
                    delimiter=',', smart_headers=False, **kwargs):
        '''Wind data import. This is a very thin wrapper on the pandas
        read_table method, with the option to pass keyword arguments to
        pandas read_table if needed.

        Parameters:
        ----------
        path: string
            Path to file to be read
        columns: tuple
            Column headers need to be a tuple of the form ('Signal', 'Height')
        header_row: int
            Row containing columns headers
        time_col: int
            Column with the timestamps
        delimiter: string, default=','
            File delimiter
        smart_headers: boolean, default False
            Uses NLTK text classifier to predict column headers

        Returns:
        --------
        DataFrame with wind data
        '''

        if time_col is None:
            raise ValueError('Please enter a value for time_col')
        
        if columns and smart_headers:
            print(('Warning: MetMast will default to user defined columns if '
                   'both the columns argument and smart_headers=True are '
                   'passed to wind_import'))

        print('Importing data...')
        self.data = pd.read_table(path, header=header_row, index_col=time_col,
                                  parse_dates=True, delimiter=delimiter,
                                  names=columns, **kwargs)

        if smart_headers and not columns:
            '''Smart parse columns for Parameters'''

            print('Parsing headers with smart_headers...')
            data_columns = self.data.columns.tolist()
            data_columns = [x.strip().lower() for x in data_columns]

            #Import NLTK classifier (see header_classifier.py)
            pkg_dir, filename = os.path.split(__file__)
            classifier_path = os.path.join(pkg_dir, 'classifier.pickle')
            with open(classifier_path, 'r') as f:
                classifier = pickle.load(f)

            #Search dict for parameter match, rename column
            sigs = ['WS', 'WD', 'TI', 'Temp', 'Rho']
            atts = ['Max', 'Min', 'Mean', 'StdDev']
            combine = [' '.join([x, y]) for x in sigs for y in atts]
            iter_dict = {}
            for sigs in combine:
                iter_dict.setdefault(sigs, 1)
            
            columns = []
            for x, cols in enumerate(data_columns):
                get_col = classifier.classify(features(cols))
                get_height = re.search(r'([0-9.]+\s*m) | ([0-9.]+\s*ft)',
                                       cols)
                if get_height:
                    height = float(re.split(r'm | ft', get_height.group())[0])
                elif self.height:
                    print(('Smart Headers could not find a height in the '
                           'header string. Defaulting to met mast "height" '
                           'attribute'))
                    height = self.height
                else:
                    print(('Smart headers could not find a height.'
                           ' Defaulting to integers.'))
                    height = iter_dict[get_col]
                new_col = '{0} {1}'.format(get_col, str(iter_dict[get_col]))
                columns.append((new_col, height))
                iter_dict[get_col] += 1
            self.data.columns = columns
            print(('The following column headers have been generated by '
                   'smart_headers:\n'))
            col_print = [x+' --> '+str(y) for x, y in zip(data_columns,
                                                          columns)]
            for x in col_print:
                print(x)
               
            #Set up data as MultiIndex for height processing 
            swp_cols = pd.MultiIndex.from_tuples([(x, y) for y, x in columns])
            self._multidata = pd.DataFrame(self.data, columns=swp_cols)

    def weibull(self, column=None, ws_intervals=1, method='EuroAtlas',
                plot='matplotlib'):
        '''Calculate distribution and weibull parameters from data

        Parameters:
        ___________
        column: string
            Column to perform weibull analysis on
        ws_intervals: float, default=1
            Wind Speed intervals on which to bin
        method: string, default 'LeastSq'
            Weibull calculation method.
        plot: string, default 'matplotlib'
            Choose whether or not to plot your data, and what method.
            Currently only supporting matplotlib, but hoping to add
            Bokeh as that library evolves.

        Returns:
        ________
        DataFrame with hourly data distributions
        '''

        ws_data = self.data[column]
        ws_range = np.arange(0, ws_data.max()+ws_intervals,
                             ws_intervals)
        binned = pd.cut(ws_data, ws_range)
        dist_10min = pd.value_counts(binned).reindex(binned.levels)
        dist = pd.DataFrame({'Binned: 10Min': dist_10min})
        dist['Binned: Hourly'] = dist['Binned: 10Min']/6
        dist = dist.fillna(0)
        normed = dist['Binned: 10Min']/dist['Binned: 10Min'].sum()
        ws_normed = normed.values
        x = np.arange(0, len(ws_normed), ws_intervals)

        if method == 'EuroAtlas':
            A, k = west.euro_atlas(ws_data)
        elif method == 'LeastSq':
            A, k = west.least_sq(ws_normed, x)

        A = round(A, 3)
        k = round(k, 3)
        rv = spystats.exponweib(1, k, scale=A, floc=0)

        if plot == 'matplotlib':
            smooth = np.arange(0, 100, 0.1)
            plottools.weibull(smooth, rv.pdf(smooth), binned=True,
                              binned_x=x, binned_data=dist['Binned: Hourly'])

        return {'Weibull A': A, 'Weibull k': k, 'Dist': dist}

    def sectorwise(self, column=None, sectors=12, plot=None, **kwargs):
        '''Bin the wind data sectorwise
        '''
        cuts = 360/sectors
        bins = [0, cuts/2]
        bins.extend(np.arange(cuts*1.5, 360-cuts, cuts))
        bins.extend([360-cuts/2, 360])
        zeroed = lambda x: 0 if x == 360 else x
        self.data[column] = self.data[column].apply(zeroed)
        cats = pd.cut(self.data[column], bins, right=False)
        array = pd.value_counts(cats).reindex(cats.levels).fillna(0)
        wind_rose = pd.Series({'[{0}, {1})'.format(360-cuts/2, 0+cuts/2):
                               array.ix[-1] + array.ix[0]})
        array = array.drop([array.index[0], array.index[-1]], axis=0)
        wind_rose = wind_rose.append(array)
        new_index = {x: y for x, y in zip(wind_rose.index,
                                          np.arange(0, 360, cuts))}
        wind_rose = wind_rose.rename(new_index)
        freq_frame = pd.DataFrame({'Counts': wind_rose,
                                   'Frequencies': wind_rose/wind_rose.sum()},
                                  index=wind_rose.index)

        if plot == 'matplotlib':
            plottools.wind_rose(freq_frame['Frequencies'].values,
                                sectors=sectors, **kwargs)
        return freq_frame

    def wind_shear(self):
        '''Calculate the wind shear across all met mast heights'''

        pass

        shear_dict = {}
        heights = self._multidata.columns.levels[0].tolist()
        for x in heights:
            filtered = self._multidata.filter(regex='Mean')
            shear_dict.setdefault(x, filtered)
