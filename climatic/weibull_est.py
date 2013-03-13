# -*- coding: utf-8 -*-
'''
Weibull Estimators
-------

A small library of tools for fitting weibull pdfs to data

'''

import scipy.stats as spystats
import scipy.optimize as spyopt
import numpy as np

#Least Squares 
def least_sq(data,x):
    '''Least squares fitting of parameters'''
    def residuals(p, y, x):
        '''Least squares residual errors'''
        A,k = p
        err = y-k/A*(x/A)**(k-1)*np.exp(-(x/A)**k)
        return err 
    param_init = [10, 2]
    plsq = spyopt.leastsq(residuals, param_init, args=(data,x))
    return plsq[0]