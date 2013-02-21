'''
Climatic
_________
A micro toolbox of wind data plotting tools

'''

import matplotlib.pyplot as plt
import numpy as np
import math 

def wind_rose(freqs, sectors=12)
    '''
    Plots a wind rose using sectorwise frequencies
    
    Parameters:
    ___________
    freqs: numpy array, list, or pandas series of float or int
        Array of frequencies to plot for wind rose
    sectors: int
        Number of sectors to plot. Must be the same as len(freqs) to
        avoid error
        
    Returns:
    ________
    Wind rose plot
    '''
    
    freqs_pct=np.array(freqs)/100 
    bins = 360/sectors 
    theta=np.array(range(0,360,bins)) 
    theta_rad = Theta*math.pi/180
    ticklabs = [str(x) for x in theta]     
    
    fig = plt.figure(figsize=(8,8))
    ax=fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)     
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1) 
    ax.set_thetagrids(Theta, labels=ticklabs)
    width = 30*math.pi/180
    adj_theta = ThetaRad-width/2
    bars = ax.bar(adj_theta, freqs_pct, width=width, bottom=0.0)
    for bar in bars:
        bar.set_alpha(0.6)
    plt.show()