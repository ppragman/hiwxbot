# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 23:59:28 2015
twitter bot hourly synopsis

@author: patrickpragman
"""

from getMetar import Metar
from fireTweet import fireTweet
    
airportlist = ['PHLI', 'PHBK', 'PHNL', 'PHJR', 'PHNL', 'PHMK', 'PHNY', 'PHOG', 'PHKO', 'PHTO']
metarList = []

for airport in airportlist:
    metarList.append(Metar(airport))

synopsis = 'Hourly HI WX Synopsis:'

for report in metarList:
    synopsis = synopsis + report.stationID + '-' + report.flightRules + ' '
    
fireTweet(synopsis)


