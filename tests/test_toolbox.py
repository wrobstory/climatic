  # -*- coding: utf-8 -*-
'''
Test Toolbox
-------

Test the toolbox module with nosetests 

'''
import pandas as pd
import numpy as np
import scipy.stats as spystats
from scipy.special import gamma
from pandas.util.testing import assert_almost_equal

from climatic import toolbox

class TestToolbox():
    '''Test the functions of the toolbox module'''
    
    def setup(self):
        bins = np.arange(0, 41, 1)
        Vmean = 8
        A = 9
        k = 2
        AVmean = Vmean/(gamma(1+1/k))
        step_size = bins[1]-bins[0]
        self.rv_A = spystats.exponweib(1, k, scale=A, floc=0)
        self.rv_Vmean = spystats.exponweib(1, k, scale=AVmean, floc=0)
        hourly_A = self.rv_A.pdf(bins)*8760*step_size
        normed_A = hourly_A/hourly_A.sum()
        hourly_Vmean = self.rv_Vmean.pdf(bins)*8760*step_size
        normed_Vmean = hourly_Vmean/hourly_Vmean.sum()
        self.hourlyA = pd.DataFrame({'Annual Hours': hourly_A,
                                     'Normalized': normed_A},
                                    index=bins)
        self.hourlyVmean = pd.DataFrame({'Annual Hours': hourly_Vmean,
                                         'Normalized': normed_Vmean},
                                        index=bins)
    
    def test_weib_hourly_Ak(self):
        self.weibull = toolbox.weibull_hourly(k=2, A=9)
        assert_almost_equal(self.weibull, self.hourlyA)