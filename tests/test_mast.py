import unittest
import pandas as pd
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
        col_names = ['WS', 'St Dev', 'Dir']
        true_df = pd.read_table(r'test_data_import.csv', header=0,
                                index_col=0,delimiter=',',
                                names=col_names)
        test_mast.wind_import(r'test_data_import.csv', header_row=0, 
                              time_col=0, delimiter=',', names=col_names)
        assert_almost_equal(true_df, test_mast.data)
        
                
def main():
    unittest.main()
    
if __name__ == '__main__':
    main()       