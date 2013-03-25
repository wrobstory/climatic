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


def weibull_hourly(k, A=None, Vmean=None, bins=np.arange(0, 41, 1), 
                   plot='matplotlib'):
    '''Calculate weibull distribution and annual hours from A, k, or
    Vmean parameters

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
    R = spystats.exponweib.rvs(1, k, scale=A, floc=0, size=30000)
    rv = spystats.exponweib(1, k, scale=A, floc=0)

    weib_frame = pd.DataFrame({'Simulated Data': R})
    hour_cut = pd.cut(weib_frame['Simulated Data'], bins, right=False)
    binned_frame = pd.value_counts(hour_cut).reindex(hour_cut.levels)
    hours = binned_frame/binned_frame.sum()*8760
    hours = hours.fillna(0)
    df_hourly = pd.DataFrame({'Annual Hours': hours,
                              'Normalized': hours/hours.sum()},
                             index=hours.index)
    step_size = bins[1]-bins[0]
    bot_bins = np.arange(0, max(bins), step_size)
    cont_bins = np.arange(0, 100, 0.1)
    if plot == 'matplotlib':
        plottools.weibull(cont_bins, rv.pdf(cont_bins), binned=True,
                          binned_x=bot_bins, binned_data=hours)
    return df_hourly
