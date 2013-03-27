
Climatic: Wind Data Visualization
=================================

A small toolbox of wind data analysis tools.

Concept
-------

A small toolbox for analyzing and plotting wind data, built on top of the Pandas
library and complete with opinionated plot styling. 

Data Import and Manipulation
-----------

``MetMast``
    A class to import and manipulate met mast data
    
* ``wind_import`` Quickly import met mast data, with smart_headers functionality
to intelligently parse headers 
* ``weibull`` Calculate weibull parameters from imported data, using least squares fitting
or the European Wind Atlas guideline
* ``sectorwise`` Bin data sectorwise

Plotting Tools
--------------

``wind_rose``
    Plot a directional wind rose with as many sectors as you like.
    
![](http://farm9.staticflickr.com/8373/8594568086_a4c31bf22a_n.jpg) 
    
``weibull``
    Plot both weibull PDF distribution and hourly distribution

![](http://farm9.staticflickr.com/8510/8594568080_1609d562f1.jpg)

Toolbox
--------------

``weibull_hourly`` 
    Calculate weibull distribution and annual hours from Weibull k and A/Vmean
    
![](http://farm9.staticflickr.com/8389/8593487567_a4317d6a3a.jpg)
