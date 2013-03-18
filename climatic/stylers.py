# -*- coding: utf-8 -*-
''''
This is a library of stylers for plots

ALL credit for rstyle and rbar goes to messymind.net:
http://messymind.net/2012/07/making-matplotlib-look-like-ggplot/

'''
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import husl


def husl_gen():
    '''Generate random set of HUSL colors, one dark, one light'''
    hue = np.random.randint(0, 360)
    saturation, lightness = np.random.randint(0, 100, 2)
    husl_dark = husl.husl_to_hex(hue, saturation, lightness/3)
    husl_light = husl.husl_to_hex(hue, saturation, lightness)
    return str(husl_dark), str(husl_light)


def rstyle(ax):
    '''Styles x,y axes to appear like ggplot2
    Must be called after all plot and axis manipulation operations have been
    carried out (needs to know final tick spacing)
    '''

    #Set the style of the major and minor grid lines, filled blocks
    ax.grid(True, 'major', color='w', linestyle='-', linewidth=1.4)
    ax.grid(True, 'minor', color='0.99', linestyle='-', linewidth=0.7)
    ax.patch.set_facecolor('0.90')
    ax.set_axisbelow(True)

    #Set minor tick spacing to 1/2 of the major ticks
    ax.xaxis.set_minor_locator((pylab.MultipleLocator((plt.xticks()[0][1]
                                - plt.xticks()[0][0]) / 2.0)))
    ax.yaxis.set_minor_locator((pylab.MultipleLocator((plt.yticks()[0][1]
                                - plt.yticks()[0][0]) / 2.0)))

    #Remove axis border
    for child in ax.get_children():
        if isinstance(child, matplotlib.spines.Spine):
            child.set_alpha(0)

    #Restyle the tick lines
    for line in ax.get_xticklines() + ax.get_yticklines():
        line.set_markersize(5)
        line.set_color("gray")
        line.set_markeredgewidth(1.4)

    #Remove the minor tick lines
    for line in (ax.xaxis.get_ticklines(minor=True) +
                 ax.yaxis.get_ticklines(minor=True)):
        line.set_markersize(0)

    #Only show bottom left ticks, pointing out of axis
    plt.rcParams['xtick.direction'] = 'out'
    plt.rcParams['ytick.direction'] = 'out'
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')


def rbar(ax, left, height, **kwargs):
    '''Creates a bar plot with default style parameters to look like ggplot2
    kwargs can be passed to changed other parameters
    '''
    defaults = {'facecolor': '0.15',
                'edgecolor': '0.28',
                'linewidth': 1,
                'width': 1}

    for x, y in defaults.iteritems():
        kwargs.setdefault(x, y)

    return ax.bar(left, height, **kwargs)


def rfill(ax, x_range, dist, **kwargs):
    '''Creates a distribution fill with default parameters to resemble ggplot2
    kwargs can be passed to change other parameters
    '''
    husl_dark_hex, husl_light_hex = husl_gen()
    defaults = {'color': husl_dark_hex,
                'facecolor': husl_light_hex,
                'linewidth': 2.0,
                'alpha': 0.2}

    for x, y in defaults.iteritems():
        kwargs.setdefault(x, y)

    return ax.fill(x_range, dist, **kwargs)


def rhist(ax, data, **kwargs):
    '''Creates a hist plot with default style parameters to look like ggplot2
    kwargs can be passed to changed other parameters
    '''
    defaults = {'facecolor': '0.15',
                'edgecolor': '0.28',
                'linewidth': 1,
                'rwidth': 1}

    for x, y in defaults.iteritems():
        kwargs.setdefault(x, y)

    return ax.hist(data, **kwargs)
