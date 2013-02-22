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

Mast1 = cl.MetMast(lat=-75.00, long=100.00)
Mast1.wind_import(r'USDOE_beresford_051201.csv', header_row=54, time_col=0,
                  delimiter=',')
Mast1.data[:50]