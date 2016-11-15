#!/usr/bin/env python
# Tides.py gets tide info from world tides and posts the next high/low tide to 20x4 LCD
import I2C_LCD_driver
import json
import time
import os
from urllib2 import urlopen
#hand=open('tide.txt')
mylcd = I2C_LCD_driver.lcd()
count =0
req = urlopen('https://www.worldtides.info/api?extremes&lat=39.378&lon=-74.504&key=a8fc6f5e-62e1-42d3-813b-927efb1782bd')
parsed_json = json.load(req)
ti = str(parsed_json["station"])

os.system('clear')
print "Tides at Ventnor Pier:"
print "----------------------"
print

x=1
for x in range (0,7):
    dt = int(parsed_json["extremes"][x]["dt"])
    ex = str(parsed_json["extremes"][x]["type"])
    ct = time.strftime("%a %b%d %H:%M ", time.localtime(dt))
    print ct,ex

print
dta = int(parsed_json["extremes"][0]["dt"])
exa = str(parsed_json["extremes"][0]["type"])
cta = time.strftime("%a %b%d %H:%M ", time.localtime(dta))


dtb = int(parsed_json["extremes"][1]["dt"])
exb = str(parsed_json["extremes"][1]["type"])
ctb = time.strftime("%a %b%d %H:%M ", time.localtime(dtb))


cxa=cta+exa
cxb=ctb+exb
print cxa
print cxb
print
mylcd.lcd_display_string("Tides at Vent Pier:", 1)
mylcd.lcd_display_string("--------------------", 2)
mylcd.lcd_display_string(cxa, 3)
mylcd.lcd_display_string(cxb, 4)
