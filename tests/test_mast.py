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

        #Set up simple import for testing
        self.simple_mast = cl.MetMast(lat=45.5236, lon=122.6750, height=80,
                                      time_zone='US/Eastern')
        col_names = ['Wind Speed 1', 'Std Dev 1', 'Wind Direction 1']
        pkg_dir, filename = os.path.split(os.path.abspath(__file__))
        simple_import = os.path.join(pkg_dir, r'data/test_data_import.csv')
        self.simple_pd = pd.read_table(simple_import, header=0,
                                       index_col=0, delimiter=',',
                                       names=col_names)
        self.simple_mast.wind_import(simple_import, columns=col_names,
                                     header_row=0, time_col=0, delimiter=',')

        #Set up the USDOE Beresford data for testing
        self.beresford = cl.MetMast()
        col_names = ['Wind Speed 1', 'Std Dev 1', 'Wind Direction 1']
        pkg_dir, filename = os.path.split(os.path.abspath(__file__))
        beres_import = os.path.join(pkg_dir,
                                    r'data/USDOE_beresford_051201.csv')
        self.beres_pd = pd.read_table(beres_import, header=57,
                                      index_col=0, delimiter=',',
                                      names=col_names)
        self.beresford.wind_import(beres_import, columns=col_names,
                                   header_row=57, time_col=0, delimiter=',',
                                   smart_headers=False)

    def test_atts(self):
        #Test for standard input

        assert self.simple_mast.lat == 45.5236
        assert self.simple_mast.lon == 122.6750
        assert self.simple_mast.height == 80
        assert self.simple_mast.time_zone == 'US/Eastern'

    def test_simple_import(self):
        '''Test the simple import vs. standard panda dataframe'''

        assert_almost_equal(self.simple_pd, self.simple_mast.data)

    def test_complex_import(self):
        '''Test a more complex import vs. standard panda dataframe'''

        assert_almost_equal(self.beres_pd, self.beresford.data)

    def test_weibull(self):
        '''Test the weibull generating method'''
        cut_bins = np.arange(0, self.beres_pd['Wind Speed 1'].max()+1, 1)
        binned = pd.cut(self.beres_pd['Wind Speed 1'], cut_bins)
        dist_10min = pd.value_counts(binned).reindex(binned.levels)
        dist = pd.DataFrame({'Binned: 10 Minute': dist_10min})
        dist['Binned: Hourly'] = dist['Binned: 10 Minute']/6
        dist = dist.fillna(0)
        weib_dict = self.beresford.weibull(column='Wind Speed 1')

        assert_almost_equal(dist, weib_dict['Dist'])
        nt.assert_almost_equal(13.278, weib_dict['Weibull A'])
        nt.assert_almost_equal(1.795, weib_dict['Weibull k'])
        
    def test_sectorwise(self):
        '''Test the sectorwise method'''
        sectors12 = self.beresford.sectorwise(column='Wind Direction 1', 
                                              sectors=12)
        sectors36 = self.beresford.sectorwise(column='Wind Direction 1', 
                                              sectors=36)
        counts = pd.value_counts(self.beresford.data['Wind Direction 1']).sum()
        
        assert sectors12['Counts'].sum() == counts
        assert sectors12['Frequencies'].sum() == 1
