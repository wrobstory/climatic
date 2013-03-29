  # -*- coding: utf-8 -*-
'''
Test Mast
-------

Test the MetMast class with nosetests

'''

from __future__ import print_function
import os
import pandas as pd
import numpy as np
import climatic as cl
import nose.tools as nt
from pandas.util.testing import assert_almost_equal


class TestMast():

    def setup(self):
        '''Setup MetMast objects for testing'''

        '''Set up simple import for testing with given columns, both with
        climatic and with pandas'''
        self.simple_mast = cl.MetMast(lat=45.5236, lon=122.675, height=80,
                                      time_zone='US/Eastern')
        self.simple_cols = [('Wind Speed 1 Mean', 50),
                            ('Wind Speed Std Dev 1', 50),
                            ('Wind Direction 1', 50),
                            ('Wind Speed 2 Mean', 40),
                            ('Wind Speed St Dev 2', 40),
                            ('Wind Speed Direction 2', 40), 
                            ('Binned Direction 1', 40)]
        pkg_dir, filename = os.path.split(os.path.abspath(__file__))
        self.simple_import = os.path.join(pkg_dir,
                                          r'data/test_data_import.csv')
        self.simple_pd = pd.read_table(self.simple_import, header=0,
                                       index_col=0, delimiter=',',
                                       names=self.simple_cols)
        self.simple_mast.wind_import(self.simple_import, 
                                     columns=self.simple_cols,
                                     header_row=0, time_col=0, delimiter=',')

        #Set up the USDOE Beresford data for testing
        self.beresford = cl.MetMast()
        self.beres_cols = [('Wind Speed 1', 66), ('Std Dev 1', 66),
                           ('Wind Direction 1', 66)]
        pkg_dir, filename = os.path.split(os.path.abspath(__file__))
        self.beres_import = os.path.join(pkg_dir,
                                         r'data/USDOE_beresford_051201.csv')
        self.beres_pd = pd.read_table(self.beres_import, header=57,
                                      index_col=0, delimiter=',',
                                      names=self.beres_cols)
        self.beresford.wind_import(self.beres_import, columns=self.beres_cols,
                                   header_row=57, time_col=0, delimiter=',',
                                   smart_headers=False)
                                   
    def test_repr(self):
        #Test repr method
        
        repr_str = ("climatic.MetMast(lat=45.5236, "
                                     "lon=122.675, "
                                     "height=80, "
                                     "time_zone='US/Eastern')")
        assert repr(self.simple_mast) == repr_str
                                              
    def test_atts(self):
        '''Test for standard input'''

        assert self.simple_mast.lat == 45.5236
        assert self.simple_mast.lon == 122.6750
        assert self.simple_mast.height == 80
        assert self.simple_mast.time_zone == 'US/Eastern'

    def test_simple_import(self):
        '''Test the simple import vs. standard panda dataframe'''

        assert_almost_equal(self.simple_pd, self.simple_mast.data)

    def test_simple_import_no_cols(self):
        '''Test import with no columns fed'''
        self.no_col_mast = cl.MetMast()
        self.no_col_mast.wind_import(self.simple_import, header_row=0,
                                     time_col=0, delimiter=',')
        self.no_col_pd = pd.read_table(self.simple_import, header=0,
                                       index_col=0, delimiter=',')

        assert_almost_equal(self.no_col_mast.data, self.no_col_pd)

    def test_complex_import(self):
        '''Test a more complex import vs. standard panda dataframe'''

        assert_almost_equal(self.beres_pd, self.beresford.data)

    def test_weibull(self):
        '''Test the weibull generating method'''
        bins = np.arange(0, self.beres_pd[('Wind Speed 1', 66)].max()+1, 1)
        binned = pd.cut(self.beres_pd[('Wind Speed 1', 66)], bins)
        dist_10min = pd.value_counts(binned).reindex(binned.levels)
        dist = pd.DataFrame({'Binned: 10 Minute': dist_10min})
        dist['Binned: Hourly'] = dist['Binned: 10 Minute']/6
        dist = dist.fillna(0)
        weib_dict = self.beresford.weibull(column=('Wind Speed 1', 66))

        assert_almost_equal(dist, weib_dict['Dist'])
        nt.assert_almost_equal(13.278, weib_dict['Weibull A'])
        nt.assert_almost_equal(1.795, weib_dict['Weibull k'])

    def test_sectorwise(self):
        '''Test the sectorwise method'''
        sectors12 = self.beresford.sectorwise(column=('Wind Direction 1', 66),
                                              sectors=12)
        sectors36 = self.beresford.sectorwise(column=('Wind Direction 1', 66),
                                              sectors=36)
        cnt = pd.value_counts(self.beresford.data[('Wind Direction 1', 66)])
        summed_counts = cnt.sum()

        assert sectors12['Counts'].sum() == summed_counts
        assert sectors12['Frequencies'].sum() == 1
        
    def test_dup_timestamps(self):
        '''Test timestamp duplicator check'''
        
        stamp = pd.Timestamp('2005/12/01 18:10:00')
        assert self.simple_mast.data_overlap()[0] == stamp
        
    def test_binned(self):
        '''Test binning functionality'''
        
        ws_bins = np.arange(0, 41, 1)
        wd_bins = np.arange(0, 375, 15)
        
        def makeindex(bins):
            step = bins[1]-bins[0]
            new_index = ['[{0}-{1}]'.format(x, x+step) for x in bins]
            new_index.pop(-1)
            return new_index
        
        ws_index = makeindex(ws_bins)
        wd_index = makeindex(wd_bins)
        self.simple_mast.binned(column=('Wind Speed 1 Mean', 50), bins=ws_bins, 
                                stat='max', name='WS1Max')
        self.simple_mast.binned(column=('Wind Direction 1', 50), bins=wd_bins, 
                                stat='mean', name='WDMean')
                                
        grouped = self.simple_mast.data.groupby([('Binned Direction 1', 40)])  
        test_mean = grouped.mean().reindex(wd_index)
                                
        assert hasattr(self.simple_mast, 'data_binned_WS1Max')
        assert len(self.simple_mast.data_binned_WS1Max) == len(ws_bins)-1
        for x in self.simple_mast.data_binned_WS1Max.iteritems():
            assert x[1].max() == self.simple_mast.data[x[0]].max()
            
        assert_almost_equal(self.simple_mast.data_binned_WDMean.dropna(), 
                            test_mean.dropna())        
        
                                
        
        
