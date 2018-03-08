#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function
import ephem
import datetime
import time
import Logger
import googlemaps



class Place():
    @staticmethod
    def FromAddress(Address):
        gclient = googlemaps.Client(key='AIzaSyA9TsRNwHTo2ktzKLtVSm9qqfc458nSYuw')
        geocoderesult = googlemaps.geocoding.geocode(gclient,Address)
        Latitude = geocoderesult[0]['geometry']['location']['lat']
        Longitude = geocoderesult[0]['geometry']['location']['lng']
        location =(Latitude, Longitude)
        elevationresult = googlemaps.elevation.elevation(gclient, location)
       
        Altitude = elevationresult[0]['elevation']
        _place = Place(Latitude, Longitude, Altitude)
        _place.Address = geocoderesult[0]['formatted_address']
        return _place



    def __init__(self, Latitude, Longitude, Altitude):
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Altitude = Altitude
        self.observer = ephem.Observer()
        self.observer.lat  = str(Latitude)
        self.observer.lon  = str(Longitude)
        self.observer.elev = Altitude

    def Sunrise(self, Day):
        self.observer.date = str(self.__local_to_utc(Day))
        Rising = self.observer.previous_rising(ephem.Sun())
        return self.__utc_to_local (Rising.datetime()) 

    def Sunset(self, Day):
        self.observer.date = str(self.__local_to_utc(Day))
        Setting = self.observer.next_setting(ephem.Sun())
        return self.__utc_to_local (Setting.datetime()) 

    def Moonrise(self, Day):
        self.observer.date = str(self.__local_to_utc(Day))
        Rising = self.observer.previous_rising(ephem.Moon())
        return self.__utc_to_local (Rising.datetime()) 

    def Moonset(self, Day):
        self.observer.date = str(self.__local_to_utc(Day))
        Setting = self.observer.next_setting(ephem.Moon())
        return self.__utc_to_local (Setting.datetime()) 
        

    def __utc_to_local(self, dt):
        return dt - datetime.timedelta(seconds = time.timezone)

    def __local_to_utc(self, dt):
        return dt + datetime.timedelta(seconds = time.timezone)



if __name__ == '__main__':

    
    SanMichele2 = Place.FromAddress('Viale Rivi 32 Sassuolo')

    sunrise = SanMichele2.Sunrise(datetime.datetime.now())
    sunset = SanMichele2.Sunset(datetime.datetime.now())
    moonrise = SanMichele2.Moonrise(datetime.datetime.now())
    moonset = SanMichele2.Moonset(datetime.datetime.now())

    print('SAN MICHELE')
    print(u'Oggi è il {:%d.%m.%Y}'.format(datetime.date.today()))
    print('Il sole sorge alle {:%H:%M}'.format(sunrise))
    print('tramonta alle {:%H:%M}'.format(sunset))

    print('La luna sorge alle {:%H:%M}'.format(moonrise))
    print('tramonta alle {:%H:%M}'.format(moonset))

    print (SanMichele2.Address)
   
    CasaLanzi = Place.FromAddress(u'Via Cà dei Lanzi 7 Carpineti')
    print (CasaLanzi.Altitude)
