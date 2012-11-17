#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import os.path
import ConfigParser
import sys

class getWeather():

    def get_city_id(self, city):
    
        city_list = ConfigParser.ConfigParser()
        city_list.read('./city-id.txt')

        try:
            city_id = city_list.get('CityList',city)
        except:    
            url = "http://openweathermap.org/data/2.0/find/name?q="+city
            try:
                f = urllib2.urlopen(url)
            except:
                print 'Error!'
            s = f.read()   
            
            city_id = s.split("\"id\":")[-1].split(",")[0]
            
            if str(city_id).isdigit():   
                output = open('./city-id.txt','a')
                output.write('\n'+city+" = "+city_id)
                output.close()
            else:
                print 'Error! There is no such city!'
                sys.exit()
                    
        return city_id


    def get_json_data(self,city):
        
        city_id = self.get_city_id(city)
            
        url = "http://openweathermap.org/data/2.0/weather/city/"+city_id+"?type=json"
        try:
            f = urllib2.urlopen(url)
        except:
            return None
        s = f.read()           
        return s

        
    def get_weather(self, city):
        
        json_data = self.get_json_data(city)
        jdata_decoded = json.loads(json_data)
        w_data = {}
        
        w_data['id'] = str(jdata_decoded['id'])
        w_data['name'] = str(jdata_decoded['name'])
        w_data['date'] = str(jdata_decoded['date'])
        w_data['temp'] = str(jdata_decoded['main']['temp'] - 273.15)+""u"\u00B0"
        w_data['pressure'] = str(jdata_decoded['main']['pressure']*0.75)+" mmHg"
        w_data['humidity'] = str(jdata_decoded['main']['humidity'])+"%"
        w_data['wind'] = str(jdata_decoded['wind']['speed'])+" m/s"
        w_data['clouds'] = str(jdata_decoded['clouds']['all'])+"%"
        w_data['rain'] = str(jdata_decoded['rain']['3h'])
        
        w_img = jdata_decoded['img']
        w_iconname = w_img.split("/")[-1]
        
        if not os.path.exists('./images/'+w_iconname):
            w_icon = urllib2.urlopen(w_img).read()
            output = open('./images/'+w_iconname,'wb')
            output.write(w_icon)
            output.close()
         
        w_data['img'] = str(w_iconname)
        
        return w_data    
    
    def main(self, city):
        
        weather_data = self.get_weather(city)
        print 'Weather in '+city+''
        print 'Temperature:',weather_data['temp']
        print 'Pressure   :',weather_data['pressure']
        print 'Humidity   :',weather_data['humidity']
        print 'Wind       :',weather_data['wind']
        print 'Clouds     :',weather_data['clouds']
        print 'Rain       :',weather_data['rain']
        

if __name__ == "__main__":

    app = getWeather()
    app.main(str(sys.argv[1]))
