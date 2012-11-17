#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import gobject
import time
from openweather import getWeather

city = 'Novosibirsk'


################
## GTK APPLET ##
################

class WeatherApp:


    def __init__(self):

        self.statusicon = gtk.StatusIcon()

        self.statusicon.connect("popup-menu", self.right_click_event)
        self.statusicon.connect("activate", self.left_click_event)

        self.update()
        gobject.timeout_add(5*60*1000,self.update)
       
        
    def right_click_event(self, icon, button, time):
        menu = gtk.Menu()

        about = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        upd = gtk.ImageMenuItem(gtk.STOCK_REFRESH) 
        forecast = gtk.ImageMenuItem("Прогноз")
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_YES,gtk.ICON_SIZE_MENU)
        forecast.set_image(img)
        edit = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
        seprt = gtk.SeparatorMenuItem()
        quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        
        about.connect("activate", self.show_about_dialog)
        upd.connect("activate", self.upd_update)
        forecast.connect("activate", self.show_forecast)
        edit.connect("activate", self.show_edit_dialog)
        quit.connect("activate", gtk.main_quit)
        
        menu.append(about)
        menu.append(upd)
        menu.append(forecast)
        menu.append(edit)
        menu.append(seprt)
        menu.append(quit)
        
        menu.show_all()
        
        menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.statusicon)
    
        
    def show_edit_dialog(self,widget):
    
        window = gtk.Window()
        window.set_title("GtkWeather")
        #window.set_default_size(250, 200)
        #window.set_icon_from_stock(gtk.STOCK_PREFERENCES,10)
        window.set_border_width(10)
        
        box1 = gtk.VBox(gtk.TRUE, 5)
        window.add(box1)
        box1.show()
        
        
        comboboxentry = gtk.combo_box_entry_new_text()
        #window.add(comboboxentry)
        comboboxentry.set_tooltip_text("Choose your sity")
        
        f = open("city-id.txt","r")
        s = f.readline()
        while s:
            s = f.readline()
            item = s.split(' ')[0]
            if item != '':
                comboboxentry.append_text(item)
        
        comboboxentry.child.connect('changed', self.changed_city)
        comboboxentry.set_active(0)
        
        box1.pack_start(comboboxentry, gtk.FALSE, gtk.FALSE, 0)
        
        window.show_all()
        
        
        
    def changed_city(self, entry):
        
        global city
        city = unicode(entry.get_text())
        print 'Выбран город', city, '.'
        
        self.update()
        return
        
    def show_forecast(self, widget):
        window = gtk.Window()
        window.set_title("GtkWeather")
        window.set_default_size(250, 200)
        window.set_border_width(10)
        
        window.show_all()
        
    
    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("GtkWeather")
        about_dialog.set_version("1.0")
        about_dialog.set_authors(["Ace-berg"])
        		
        about_dialog.run()
        about_dialog.destroy()

    def left_click_event(self, data=None):
        
        app = getWeather()
        weather_data = app.get_weather(city)
        
        window = gtk.Window()
        window.set_title("GtkWeather")
        window.set_default_size(250, 200)
        window.set_border_width(10)
        
        image = gtk.Image()
        image.set_from_file('images/'+weather_data['img'])
        
        weather = 'Weather in '+weather_data['name']+'\n\nTemperature: '+weather_data['temp']\
                +'\nPressure      : '+weather_data['pressure']+'\nHumidity      : '+weather_data['humidity']\
                +'\nWind             : '+weather_data['wind']+'\nClouds          : '+weather_data['clouds']\
                +'\nRain              : '+weather_data['rain']
        text = gtk.Label(weather)
        
        fix = gtk.Fixed()   
        fix.put(image, 0, 0)
        fix.put(text, 40, 50)
        
        window.add(fix)
        
        
        
        window.show_all()
        


    def update(self):
        
        app = getWeather()
        weather_data = app.get_weather(city)
        
        self.statusicon.set_tooltip(weather_data['name']+', '+weather_data['temp'])
        self.statusicon.set_from_file('images/'+weather_data['img'])
        
        return 1
        
    def upd_update(self, widget):

        self.update()

    def main(self):

        self.statusicon.set_visible(True)
        gtk.main()


##################
## MAIN PROGRAM ##
##################

if __name__ == "__main__":

    app = WeatherApp()
    app.main()
