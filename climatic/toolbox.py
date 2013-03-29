  # -*- coding: utf-8 -*-
'''
Toolbox
-------

A set of small tools for wind data analysis

'''
import pandas as pd
import numpy as np
import scipy.stats as spystats
from scipy.special import gamma
import plottools


def weibull_hourly(k=None, A=None, Vmean=None, bins=np.arange(0, 41, 1),
                   plot='matplotlib'):
    '''Calculate weibull distribution and annual hours from weibull k and A or
    Vmean parameters. This distribution is based on multiplying the
    PDF by the annual hours for each wind speed bin. Defaults to Vmean for
    calculation of A if both Vmean and A are provided.

    Parameters:
    ----------
    k: float, int
        Weibull k parameters
    A: float, int
        Weibull A parameter
    Vmean: float, int
        Mean wind speed, for calculating weibull with Vmean and k only
    bins: array, default np.arange(0, 41, 1)
        Wind speed bins for estimating and plotting weibull
    plot: string, default 'matplotlib'
        Choose whether or not to plot your data, and what method.
        Currently only supporting matplotlib, but hoping to add
        Bokeh as that library evolves.

    Returns:
    ________
    Dataframe of wind-speed binned annual hours and normed values
    '''

    if Vmean:
        A = Vmean/(gamma(1+1/k))

    step_size = bins[1]-bins[0]
    rv = spystats.exponweib(1, k, scale=A, floc=0)
    hourly = rv.pdf(bins)*8760*step_size
    df_hourly = pd.DataFrame({'Annual Hours': hourly,
                              'Normalized': hourly/hourly.sum()},
                             index=bins)
    cont_bins = np.arange(0, 100, 0.1)
    if plot == 'matplotlib':
        plottools.weibull(cont_bins, rv.pdf(cont_bins), binned=True,
                          binned_x=bins, binned_data=hourly, align='center')
    return df_hourly
