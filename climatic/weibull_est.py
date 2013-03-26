  # -*- coding: utf-8 -*-
'''
Weibull Estimators
-------

A small library of tools for fitting weibull pdfs to data

'''
from __future__ import division
import scipy.optimize as spyopt
from scipy.special import gamma
import numpy as np


#Least Squares
def least_sq(data, x):
    '''Least squares fitting of parameters via data fitting to the
    distribution
    '''
    def residuals(p, y, x):
        '''Least squares residual errors'''
        A, k = p
        err = y-k/A*(x/A)**(k-1)*np.exp(-(x/A)**k)
        return err
    param_init = [10, 2]
    plsq = spyopt.leastsq(residuals, param_init, args=(data, x))
    return plsq[0]


def euro_atlas(ws_data):
    '''European Wind Atlas approach for calculating weibull parameters.
    This approach specifies the following contraints:

    - The total wind energy in the fitted weibull distribution must be equal
    to that of the observed distribution
    -The frequency of occurence of the wind speeds higher than the observed
    average speeds are the same for the two distributions

    These details can be found on pages 168-169 in the EMD WindPro manual:
    http://www.emd.dk/files/windpro2.8/WindPRO28_Manual.pdf

    '''

    #Statistical 3rd order moment
    a3 = np.sum(ws_data**3)/len(ws_data)

    #Probability of exceeding mean value
    exceed = ws_data.where(ws_data > ws_data.mean(), None)
    prob_exceed = exceed.count()/len(ws_data)

    def k_eq(x, ws_mean, a3, prob):
        '''Equation for k'''
        return np.exp(-(ws_mean/(a3/gamma(1+3/x))**(1/3))**x)-prob

    #Solve for k
    soln = spyopt.fsolve(k_eq, x0=[2], args=(ws_data.mean(), a3, prob_exceed))
    k = soln[0]

    #Solve for A
    A = (a3/gamma(1+3/k))**(1/3)

    return A, k
