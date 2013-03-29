# -*- coding: utf-8 -*-
'''
MetMast Example: Loading data into a Met Mast object.

This data and software ("Data") is provided by the National Renewable Energy
Laboratory ("NREL"), which is operated by the Alliance for Sustainable Energy,
LLC ("ALLIANCE") for the U.S. Department of Energy ("DOE"). The data can be
downloaded from the following location:
http://www.windpoweringamerica.gov/anemometerloans/projects.asp

Please see LICENSE.txt in the Examples folder for the data use
disclaimer.

The USDOE examples are measured in mph, but until better (free) met data 
can be acquired, we're going to treat them as m/s
'''

import climatic as cl

#Create Met Mast object
my_mast = cl.MetMast(lat=46.9083, lon=109.808, height=20)

#Upload your wind data
my_mast.wind_import(r'USDOE_beresford_051201.csv', header_row=54, time_col=0,
                    delimiter=',', smart_headers=True)

#Reload your data without "smart columns"
my_mast_2 = cl.MetMast()
met_columns = [('WS Mean 1', 20), ('WD Mean 1', 20), 
               ('WS StDev 1', 20)]
my_mast_2.wind_import(r'USDOE_beresford_051201.csv', columns=met_columns, 
                      header_row=54, time_col=0, delimiter=',')

#Calculate and plot weibull parameters
weibull = my_mast.weibull(column=('WS Mean 1', 20), plot='matplotlib')

#Calculate and plot sectorwise wind direction frequencies
wind_rose = my_mast.sectorwise(column=('WD Mean 1', 20), plot='matplotlib')
