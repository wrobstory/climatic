import unittest

from climatic import MetMast

class TestMast(unittest.TestCase):

    def test_latlon(self):
        #Test for standard input
        test_mast = MetMast(lat=45.5236, lon=122.6750, height=80, 
                            time_zone='US/Eastern')
        self.assertEqual(test_mast.lat, 45.5236)
        self.assertEqual(test_mast.lon, 122.6750)
        self.assertEqual(test_mast.height, 80)
        self.assertEqual(test_mast.time_zone, 'US/Eastern')
                
def main():
    unittest.main()
    
if __name__ == '__main__':
    main()       