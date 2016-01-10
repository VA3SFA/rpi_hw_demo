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
import re
import feedparser
import json
import textwrap
from HTMLParser import HTMLParser
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
    fn = os.path.expanduser('~/.EPDRSS')
    if os.path.exists(fn):
        f = open(fn, 'r')
        r = json.load(f)
        f.close()
        return r
    else:
        print "Creating default configuration file."
        f = open(fn, 'w+')
        w = {'RSS':[
                    'http://rss.cbc.ca/lineup/topstories.xml',
                    'http://rss.slashdot.org/Slashdot/slashdotMain',
                    'http://www.reddit.com/.rss']}
        json.dump(w, f)
        f.close()
        return w

def strip_tags(html):
    return re.sub('<[^>]*>', '', html)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

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
    lmin = datetime.today().minute

    conf = get_config()

    while True:
        for rss_url in conf["RSS"]:       
            feed = feedparser.parse(rss_url)
            for item in feed["items"]:
                now = datetime.today()
                draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
                draw.text((0, 150), '{c:s}'.format(c=counter), fill=BLACK, font=wfont)
                draw.text((0, 160), '{h:02d}:{m:02d}:{s:02d}'.format(h=now.hour, m=now.minute, s=now.second), fill=BLACK, font=wfont)
                ttl = strip_tags(item["title"])
                ttl.strip()
                sum = strip_tags(item["summary"])
		sum.strip()
                y = -20
                for line in textwrap.wrap(ttl, 20):
                    y += 20
                    if y < 150:
                        draw.text((0, y), line, fill=BLACK, font=font)
                y += 10
                for line in textwrap.wrap(sum, 40):
                    y += 10
                    if y < 150:
                        draw.text((0, y), line, fill=BLACK, font=wfont)
        
                # display image on the panel
                epd.display(image)
                epd.partial_update()
                time.sleep(30)
    
# main
if "__main__" == __name__:
    main()
