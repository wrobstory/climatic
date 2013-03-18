from __future__ import print_function
import unittest
import os
import pandas as pd
import numpy as np
from climatic import MetMast
from pandas.util.testing import assert_almost_equal

class TestMast(unittest.TestCase):

    def test_atts(self):
        #Test for standard input
        test_mast = MetMast(lat=45.5236, lon=122.6750, height=80, 
                            time_zone='US/Eastern')
        self.assertEqual(test_mast.lat, 45.5236)
        self.assertEqual(test_mast.lon, 122.6750)
        self.assertEqual(test_mast.height, 80)
        self.assertEqual(test_mast.time_zone, 'US/Eastern')
        
    def test_import(self):
        '''Test the importer vs. standard panda dataframe using
        pandas testing suite'''
        test_mast = MetMast()
        col_names = ['Wind Speed 1', 'Std Dev 1', 'Wind Direction 1']
        pkg_dir, filename = os.path.split(os.path.abspath(__file__))
        test_import = os.path.join(pkg_dir, r'data/test_data_import.csv')
        true_df = pd.read_table(test_import, header=0,
                                index_col=0,delimiter=',',
                                names=col_names)
        test_mast.wind_import(test_import, header_row=0, 
                              time_col=0, delimiter=',', names=col_names)
        assert_almost_equal(true_df, test_mast.data)
        
    def test_weibull(self):
        '''Test the weibull generating method'''
        test_mast = MetMast()
        col_names = ['Wind Speed 1', 'Std Dev 1', 'Wind Direction 1']
        pkg_dir, filename = os.path.split(os.path.abspath(__file__))
        test_import = os.path.join(pkg_dir, 
                                   r'data/USDOE_beresford_051201.csv')
        true_df = pd.read_table(test_import, header=54,
                                index_col=0,delimiter=',',
                                names=col_names)
        cut_bins = np.arange(0,true_df['Wind Speed 1'].max()+1,1)
        binned = pd.cut(true_df['Wind Speed 1'], cut_bins)
        dist_10min = pd.value_counts(binned).reindex(binned.levels)
        dist = pd.DataFrame({'Binned: 10 Minute': dist_10min})
        dist['Binned: Hourly'] = dist['Binned: 10 Minute']/6
        dist = dist.fillna(0)
        test_mast.wind_import(test_import, header_row=54, 
                              time_col=0, delimiter=',', names=col_names)
        weib_dict = test_mast.weibull(column='Wind Speed 1')
        assert_almost_equal(dist, weib_dict['Dist'])
        self.assertAlmostEqual(13.269, weib_dict['Weibull A'])
        self.assertAlmostEqual(1.793, weib_dict['Weibull k'])
        
                
def main():
    unittest.main()
    
if __name__ == '__main__':
    main()       