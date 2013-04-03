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
from collections import Counter
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
                    delimiter=',', smart_headers=False, subs=None, **kwargs):
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
        subs: dict, default None
            dict of regex substitutions to make in the header. Optional. 
            Ex: subs = {'Ch1': 'WS', 'Ch2': WD}
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
          
                                  
        if not isinstance(self.data.index, pd.DatetimeIndex):
            try: 
                self.data.index = self.data.index.to_datetime()
            except ValueError: 
                print(('Timestamp column not converting correctly. Iterating'
                       ' through index to check timestamp validity...'))
                for num, index in enumerate(self.data.index): 
                    try: 
                        pd.Timestamp(index)
                    except ValueError: 
                        stamps = (index, 
                                  self.data.index[num-1], 
                                  self.data.index[num+1])
                        print(('Cannot parse {0}. Previous timestamp is {1}. ' 
                               'Next timestamp is {2}.').format(stamps[0],
                                                                stamps[1],
                                                                stamps[2]))
                
        if smart_headers and not columns:
            '''Smart parse columns for Parameters'''

            print('Parsing headers with smart_headers...')
            data_columns = self.data.columns.tolist()
            #Replace with sub'd values if given
            if subs: 
            #Need to refactor this at some point...
                temp = []
                for col in data_columns: 
                    for key, value in subs.iteritems(): 
                        if re.match(key, col):
                            temp.append(re.sub(key, value, col))  
                data_columns = temp       
            
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
                get_height = re.search(r'([0-9.]+\s*m)|([0-9.]+\s*ft)',
                                       cols)
                if get_height:
                    height = float(re.split(r'm|ft', get_height.group())[0])
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
        column: tuple, default None
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
                              binned_x=x, binned_data=dist['Binned: Hourly'],
                              align='edge')

        return {'Weibull A': A, 'Weibull k': k, 'Dist': dist}

    def sectorwise(self, column=None, sectors=12, plot='matplotlib', **kwargs):
        '''Bin and plot the data sectorwise
        
        Parameters:
        ___________
        column: tuple, default None
            Column to perform sectorwise analysis on
        sectors: int, default 12
            Number of sectors to bin
        plot: string, default 'matplotlib'
            Choose whether or not to plot your data, and what method.
            Currently only supporting matplotlib, but hoping to add
            Bokeh as that library evolves.

        Returns:
        ________
        DataFrame with sectorwise distribution
        
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
            
    def data_overlap(self):
        '''Check for duplicated timestamps'''
        repeated = [date for date, count in \
                     Counter(self.data.index).iteritems() if count > 1]
        for x in repeated: 
            print('The timestamp {0} repeats in this dataset.'.format(x))
        return repeated
        
    def binned(self, column=None, bins=None, stat='mean', name=None, 
               plot=None):
        '''Bin all data based on a single column. 
        
        Parameters: 
        ___________
        column: tuple, default None
            Column on which to bin data
        bins: array, default None
            List or np.array with bins
        stat: string, default 'mean'
            Statistic you want to perform on binned data (mean, max, etc)
        name: string, default None
            Attribute name for binned data. Will create a new MetMast 
            attribute with binned data. 
        plot: tuple, default None
            If you are binning by direction, plot=column_name will pass the 
            data to plottools.wind_rose
            
        Returns: 
        ________
        self.data_binned_name, DataFrame with data summed by bins/stat
        
        Examples:
        _________
        >>> mast.binned(column=('WS Mean 1', 56), bins=np.arange(0, 41, 1))
        >>> mast.data_binned

        >>> mast.binned(column=('WD Mean 1', 56), bins=np.arange(0, 375, 15), 
                        stat='max', name='WD1_Max', plot=('WS Mean 1', 56))
        >>> mast.data_binned_WD1_Max
        
        
        '''
        print('Mapping bins to data...')
        def map_bin(x, bins):
            kwargs = {}
            if x == max(bins):
                kwargs['right'] = True
            bin = bins[np.digitize([x], bins, **kwargs)[0]]
            bin_lower = bins[np.digitize([x], bins, **kwargs)[0]-1]
            return '[{0}-{1}]'.format(bin_lower, bin)
    
        step = bins[1]-bins[0]
        new_index = ['[{0}-{1}]'.format(x, x+step) for x in bins]
        new_index.pop(-1)
    
        temp_df = self.data.dropna()
        temp_df['Binned'] = temp_df[column].apply(map_bin, bins=bins)
        grouped = temp_df.groupby('Binned')
        grouped_stat = getattr(grouped, stat)()
        grouped_stat = grouped_stat.reindex(new_index)
        if name is not None: 
            attr_name = 'data_binned_{0}'.format(name)
        else: 
            attr_name = 'data_binned'
        setattr(self, attr_name, grouped_stat)
        
        if plot: 
            sect = len(new_index)
            plottools.wind_rose(grouped_stat[plot].tolist(), sectors=sect)
            
