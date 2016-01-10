#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2015 Pervasive Displays, Inc.
# Copyright 2015-2016, Syed Faisal Akber
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.


import sys
import os
import time
import urllib2
import cStringIO
import json
from datetime import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
from EPD import EPD
import socket
import fcntl
import struct

def get_config():
    fn = os.path.expanduser('~/.EPDWeather')
    if os.path.exists(fn):
        f = open(fn, 'r')
        r = json.load(f)
        f.close()
        return r
    else:
        print "Creating Config File with Defaults"
        f = open(fn, 'w+')
        w = {'weather':{'apikey':'CHANGEME',
             'urlbase' : 'http://api.openweathermap.org/data/2.5/',
             'cities':[ 'Toronto,Canada', 
                        'Ottawa,Canada',
                        'Halifax,Canada',
                        'Vancouver,Canada',
                        'NewYork,NewYork,USA',
                        'SanFrancisco,California,USA',
                        'SanJose,California,USA',
                        'PaloAlto,California,USA', 
                        'LosAngeles,California,USA',
                        'Cancun,Mexico',
                        'Dubai,UAE',
                        'Mecca,SaudiArabia',
                        'Karachi,Pakistan',
                        'London,UK',
                        'Gothenburg,Sweden',
                        'Positano,Italy',
                        'Cork,Ireland',
                        'Cairo,Egypt',
                        'CapeTown,SouthAfrica',
                        'Nairobi,Kenya',
                        'Beijing,China',
                        'Tokyo,Japan',
                        'KualaLumpur,Malaysia',
                        'Bali,Indonesia']}}
        json.dump(w,f)
        f.close()
        return w
	
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def get_weather(city, urlbase, apikey):
    url = urlbase + 'weather?q=' + city + '&APPID=' + apikey
    req = urllib2.Request(url)
    f = urllib2.urlopen(req)
    j = json.load(f)
#   return u"%s: %s %d°C" % (j["name"], j["weather"][0]["description"], j["main"]["temp"] - 273.15)
    j["iconlink"] = 'http://openweathermap.org/img/w/' + j["weather"][0]["icon"] + '.png'
    return j


WHITE = 1
BLACK = 0

# fonts are in different places on Raspbian/Angstrom so search
possible_fonts = [
    '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono-Bold.ttf',   # R.Pi
    '/usr/share/fonts/truetype/freefont/FreeMono.ttf',                # R.Pi
    '/usr/share/fonts/truetype/LiberationMono-Bold.ttf',              # B.B
    '/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf'               # B.B
    '/usr/share/fonts/TTF/FreeMonoBold.ttf',                          # Arch
    '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf'                        # Arch
]


FONT_FILE = ''
for f in possible_fonts:
    if os.path.exists(f):
        FONT_FILE = f
        break

if '' == FONT_FILE:
    raise 'no font file found'

FONT_SIZE = 20

def main():
    """main program - draw and display a test image"""

    conf = get_config()
    apikey = conf["weather"]["apikey"]
    urlbase = conf["weather"]["urlbase"]

    epd = EPD()

    print('panel = {p:s} {w:d} x {h:d}  version={v:s} COG={g:d} FILM={f:d}'.format(p=epd.panel, w=epd.width, h=epd.height, v=epd.version, g=epd.cog, f=epd.film))
    epd.clear()

    # initially set all white background
    image = Image.new('1', epd.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)
    width, height = image.size

    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)
    wfont = ImageFont.truetype(FONT_FILE, FONT_SIZE/2)

    counter = get_ip_address('eth0')

    cities = conf["weather"]["cities"]

    while True:
        for city in cities:
            weather = get_weather(city, urlbase, apikey)
            temp =  u"%d°C" % (weather["main"]["temp"] - 273.15)

            fp = urllib2.urlopen(weather["iconlink"])
            f = cStringIO.StringIO(fp.read())
            pic = Image.open(f)
            pic = ImageOps.grayscale(pic)
            rs = pic.resize((epd.width/2, epd.height/2))
            bw = rs
    
            now = datetime.today()
            draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
            draw.text((0, 150), '{c:s}'.format(c=counter), fill=BLACK, font=wfont)
            draw.text((0, 160), '{h:02d}:{m:02d}:{s:02d}'.format(h=now.hour, m=now.minute, s=now.second), fill=BLACK, font=wfont)
            draw.text((0, 0), weather["name"], fill=BLACK, font=font)
            draw.text((0, 20), temp, fill=BLACK, font=font)
            draw.text((0, 50), weather["weather"][0]["description"], fill=BLACK, font=font)
    
            image.paste(bw, (epd.width - epd.width/2, epd.height - epd.height/2))
        
            # display image on the panel
            epd.display(image)
            epd.partial_update()
    	    time.sleep(10)
    
# main
if "__main__" == __name__:
    main()
