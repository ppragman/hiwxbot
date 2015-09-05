# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 19:04:29 2015
getMetar
This is my list of functions to grab metar data from the NWS and return it to
the user.
@author: patrickpragman
"""

#I use this package to pull data from the NWS.
import requests

#I use this package to parse the XML that the NWS sends me.
import xml.etree.ElementTree as ET


#let's create a Metar class that we can use to send parsed metar data back to the user
class Metar:
    'common class for all Metars'            
    
    def __init__(self,stationID):
        
        self.stationID =''
        self.observationTime =''
        self.temp = 0 
        self.dewpoint = 0
        self.windDirection = ''
        self.windSpeed = ''
        self.windGusts = 'No Gusts'
        self.visibility = 0
        self.wxString = ''
        self.altimeterSetting = 29.92
        self.skyCover = ''
        self.lowestCeiling = 9999999
        self.flightRules = ''
        self.rawReport = ''
        self.latitude = 0
        self.longitude = 0
        self.reporting = True
            
        #build up the URL to request the data
        baseURL = 'http://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=3&mostRecent=true&stationString='
        wholeURL = baseURL + stationID
        
        #pull the metar from the aviationweather.gov
        rawMetarRequest = requests.get(wholeURL)    
        metarTree = ET.fromstring(rawMetarRequest.text)
            

        #let's loop through the file and parse all the the tags
        for child in metarTree.iter():
                        
            #first bit of error checking, let's see if we actually got a metar
            if child.tag == 'data':
                #Let's check to see if the user called a station that's providing a report
                if child.attrib['num_results'] == '0':
                    print('No data returned for this station.')
                    self.reporting = False

        
            if child.tag == 'error':
                print('There was an error with the data from NWS')
                print(child.text)
                    
            
            #each one of these identifies which part of the XML we're working with
            #then proceeds to fill in the object we created earlier
            if child.tag == 'station_id':
                self.stationID = child.text

            if child.tag == 'observation_time':
                self.observationTime = child.text
            
            if child.tag == 'temp_c':
                self.temp = float(child.text)

            if child.tag == 'dewpoint_c':
                self.dewpoint = float(child.text)
            
            if child.tag == 'wind_dir_degrees':
                self.windDirection = child.text
            
            if child.tag == 'wind_speed_kt':
                self.windSpeed = child.text
            
            if child.tag == 'wind_gust_kt':
                self.windGusts = 'Gusting' + child.text + 'KT'
            
            if child.tag == 'visibility_statute_mi':
                self.visibility = float(child.text)
                
            if child.tag == 'altim_in_hg':
                self.altimeterSetting = float(child.text)
            
            if child.tag == 'raw_text':
                self.rawReport = child.text
                
            if child.tag == 'wx_string':
                self.wxString = child.text

            if child.tag == 'flight_category':
                self.flightRules = child.text
                
            if child.tag == 'sky_condition':

                if (child.attrib['sky_cover'] == 'SKC') or (child.attrib['sky_cover'] == 'CLR'):
                    self.skyCover = 'CLR'
                else:
                    #add the cloud type and the altitude to the string which defines the sky cover
                    self.skyCover = self.skyCover + child.attrib['sky_cover'] + ' at ' + child.attrib['cloud_base_ft_agl'] + 'ft, '

                    #Is the sky condition Broken or Overcast (the definition of a ceiling)                
                    if (child.attrib['sky_cover'] == 'BKN') or (child.attrib['sky_cover'] == 'OVC'):
                        #Is this broken or overcast layer less than what was previously recorded
                        if int(child.attrib['cloud_base_ft_agl']) < self.lowestCeiling:
                            #if it is, set the lowest ceiling to this new number
                            self.lowestCeiling = int(child.attrib['cloud_base_ft_agl'])
                
                #handle the special case of "Vertical Visibility
                if child.attrib['sky_cover'] == 'OVX':
                    self.skyCover = 'Vertical visibility '
            
            if child.tag == 'vert_vis_ft':
                self.skyCover = self.skyCover + child.text + ' ft'
                self.lowestCeiling = int(child.text)
                
            
            #get the latitude and longitude of the station
            if child.tag == 'latitude':
                self.latitude = float(child.text)
            
            if child.tag == 'longitude':
                self.longitude = float(child.text)
            

    def printMetar(self):
        print(self.stationID)
        print(self.observationTime)
        print(self.windDirection, 'at', self.windSpeed, 'KT,', self.windGusts)
        print(self.visibility, 'SM')
        print(self.wxString)
        print(self.skyCover)
        print('Temperature:',self.temp,'°C, Dewpoint:',self.dewpoint,'°C')
        print('Altimeter',self.altimeterSetting)
        print('Lowest Ceiling:',self.lowestCeiling, 'ft')
        print('Flight Rules:',self.flightRules)
        print('Raw Metar Report:\n',self.rawReport)                 


    def findNearMe(homeDrome,radius):
        #First we have to figure out the Lat-Lons of the airport you're requesting this from
        baseURL = 'http://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=stations&requestType=retrieve&format=xml&stationString='
        wholeURL = baseURL + homeDrome

    
        stationDataRequest = requests.get(wholeURL)
        stationTree = ET.fromstring(stationDataRequest.text)
        
        ctrLat = ''
        ctrLon = ''   
    
        #parse the XML, pull the local lat-lons from it
        for entry in stationTree.iter():
            if entry.tag == 'latitude':
                ctrLat = entry.text
            if entry.tag == 'longitude':
                ctrLon = entry.text

        baseURL = 'http://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=stations&requestType=retrieve&format=xml&radialDistance='
        wholeURL = baseURL + str(radius) + ';' + ctrLon + ','+ ctrLat
    
        stationDataRequest = requests.get(wholeURL)
        stationTree = ET.fromstring(stationDataRequest.text)

        airportList = []
    
        for entry in stationTree.iter():
            if entry.tag == 'station_id':
                airportList.append(entry.text)
            
    
        return airportList

    def getStationLatLons(station):
        baseURL = 'http://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=stations&requestType=retrieve&format=xml&stationString='
        wholeURL = baseURL + station

    
        stationDataRequest = requests.get(wholeURL)
        stationTree = ET.fromstring(stationDataRequest.text)

        latitude = ''
        longitude = ''

        #parse the XML, pull the local lat-lons from it
        for entry in stationTree.iter():
            if entry.tag == 'latitude':
                latitude = float(entry.text)
            if entry.tag == 'longitude':
                longitude = float(entry.text)
        
        return (latitude,longitude)
