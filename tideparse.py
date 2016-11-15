#!/usr/bin/env python
import json
import time
from urllib2 import urlopen
hand=open('tide.txt')
count =0
req = urlopen('https://www.worldtides.info/api?extremes&lat=39.428450&lon=-74.495708&key=a8fc6f5e-62e1-42d3-813b-927efb1782bd')
parsed_json = json.load(req)
ti = str(parsed_json["station"])
print
x=1
for x in range (0,4):
    dt = int(parsed_json["extremes"][x]["dt"])
    ex = str(parsed_json["extremes"][x]["type"])
    ct = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(dt))
    print ct, ex
print
