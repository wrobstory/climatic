# -*- coding: utf-8 -*-
'''
MetMast Example: Loading data into a Met Mast object. 

This data and software ("Data") is provided by the National Renewable Energy
Laboratory ("NREL"), which is operated by the Alliance for Sustainable Energy,
LLC ("ALLIANCE") for the U.S. Department of Energy ("DOE"). The data can be
downloaded from the following location: 
http://www.windpoweringamerica.gov/anemometerloans/projects.asp

Please see LICENSE.txt in the Examples folder for the data use
disclaimer

'''

import climatic as cl

#Create Met Mast object
my_mast = cl.MetMast(lat=-75.00, lon=100.00)

#Upload your wind data
my_mast.wind_import(r'USDOE_beresford_051201.csv', header_row=54, time_col=0,
                    delimiter=',')
                    
#Calculate your weibull parameters and plot your data
weibull_pars=my_mast.weibull(column='Wind Speed 1', plot='matplotlib')

#Reload your data without "smart columns"
my_mast_2 = cl.MetMast()
my_mast_2.wind_import(r'USDOE_beresford_051201.csv', header_row=54, time_col=0,
                      delimiter=',', smart_headers=False)