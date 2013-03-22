# -*- coding: utf-8 -*-
'''
Toolbox Examples:

weibull_hourly: estimate the annual hours in each wind speed bin based on
                weibull k and A/Vmean


'''

import climatic as cl

#Using weibull A
hour_distribution = cl.toolbox.weibull_hourly(2.0, A=9.0)

#Using weibull k
hour_distribution = cl.toolbox.weibull_hourly(2.0, Vmean=8.0)
