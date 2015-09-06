# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 16:47:51 2015
HI Metar Twitterbot weather checker and poster

@author: patrickpragman
"""
from getMetar import Metar
from fireTweet import fireTweet

    
airportlist = ['PHLI', 'PHBK', 'PHNL', 'PHJR', 'PHNL', 'PHMK', 'PHNY', 'PHOG', 'PHKO', 'PHTO']
metarList = []

for airport in airportlist:
    metarList.append(Metar(airport))


for report in metarList:    
        
    if report.flightRules == 'IFR':
        fireTweet('Warning! ' + report.stationID + ' reporting ' + report.flightRules)
        fireTweet(report.rawReport)
    
    if report.flightRules == 'LIFR':
        fireTweet('Warning! ' + report.stationID + ' reporting ' + report.flightRules)
        fireTweet(report.rawReport)




