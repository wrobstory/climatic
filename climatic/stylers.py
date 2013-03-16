# -*- coding: utf-8 -*-
''''
This is a library of stylers for plots

ALL credit for rstyle and rbar goes to messymind.net: 
http://messymind.net/2012/07/making-matplotlib-look-like-ggplot/

'''
from pylab import *
import pdb

def rstyle(ax): 
    """Styles an axes to appear like ggplot2
    Must be called after all plot and axis manipulation operations have been 
    carried out (needs to know final tick spacing)
    """
    #set the style of the major and minor grid lines, filled blocks
    ax.grid(True, 'major', color='w', linestyle='-', linewidth=1.4)
    ax.grid(True, 'minor', color='0.99', linestyle='-', linewidth=0.7)
    ax.patch.set_facecolor('0.94')
    ax.set_axisbelow(True)
    
    #set minor tick spacing to 1/2 of the major ticks
    ax.xaxis.set_minor_locator((MultipleLocator((plt.xticks()[0][1]
                                -plt.xticks()[0][0]) / 2.0 )))
    ax.yaxis.set_minor_locator((MultipleLocator((plt.yticks()[0][1]
                                -plt.yticks()[0][0]) / 2.0 )))
    
    #remove axis border
    for child in ax.get_children():
        if isinstance(child, matplotlib.spines.Spine):
            child.set_alpha(0)
       
    #restyle the tick lines
    for line in ax.get_xticklines() + ax.get_yticklines():
        line.set_markersize(5)
        line.set_color("gray")
        line.set_markeredgewidth(1.4)
    
    #remove the minor tick lines    
    for line in (ax.xaxis.get_ticklines(minor=True) + 
                 ax.yaxis.get_ticklines(minor=True)):
        line.set_markersize(0)
    
    #only show bottom left ticks, pointing out of axis
    rcParams['xtick.direction'] = 'out'
    rcParams['ytick.direction'] = 'out'
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    
    if ax.legend_ <> None:
        lg = ax.legend_
        lg.get_frame().set_linewidth(0)
        lg.get_frame().set_alpha(0.5)
        
def rbar(ax, left, height, **keywords):
    """Creates a histogram with default style parameters to look like ggplot2
    Is equivalent to calling ax.hist and accepts the same keyword parameters.
    If style parameters are explicitly defined, they will not be overwritten
    """
    defaults = {'facecolor' : '0.3',
                'edgecolor' : '0.28',
                'linewidth' : 1, 
                'width': 1}
                            
    for x,y in defaults.iteritems():
        keywords.setdefault(x, y)
    
    return ax.bar(left, height, **keywords)

         
        

