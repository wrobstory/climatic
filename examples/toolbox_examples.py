# -*- coding: utf-8 -*-
'''
Toolbox Examples:

weibull_hourly: estimate the annual hours in each wind speed bin based on
                weibull k and A/Vmean


'''

from climatic import toolbox

#Using weibull A
hour_distribution1 = toolbox.weibull_hourly(2.0, A=9.0)

#Using weibull k
hour_distribution2 = toolbox.weibull_hourly(2.0, Vmean=8.0)
