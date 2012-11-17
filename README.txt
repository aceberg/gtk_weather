Gtk_weather consists of two python scripts:
1. openweather.py - is a command-line tool to grab weather for your City. Example:

$ ./openweather.py Novosibirsk
Weather in Novosibirsk
Temperature: -4.0°
Pressure   : 759.75 mmHg
Humidity   : 92.2%
Wind       : 1 m/s
Clouds     : 96%
Rain       : 1


2. weather_widget.py - gui tray icon. Launch it:

./weather_widget.py &
