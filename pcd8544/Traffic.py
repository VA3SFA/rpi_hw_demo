#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2015 Pervasive Displays, Inc.
# Copyright 2015, Syed Faisal Akber
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
from PIL import Image
from PIL import ImageOps
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

cams = ['http://www.mtocdn.ca/english/traveller/compass/camera/pictures/BurlCamera/loc20.jpg?1448639401',
        'http://www.mtocdn.ca/english/traveller/compass/camera/pictures/BurlCamera/loc27.jpg?1448639401',
        'http://www.mtocdn.ca/english/traveller/compass/camera/pictures/BurlCamera/loc29.jpg?1448639401',
        'http://www.mtocdn.ca/english/traveller/compass/camera/pictures/BurlCamera/loc31.jpg?1448639401',
        'http://www.mtocdn.ca/english/traveller/compass/camera/pictures/BurlCamera/loc32.jpg?1448639401',
        'http://www.mtocdn.ca/english/traveller/compass/camera/pictures/BurlCamera/loc33.jpg?1448639401',
        'http://www.mtocdn.ca/english/traveller/compass/camera/pictures/BurlCamera/loc68.jpg?1448639401',
        'http://www.mtocdn.ca/english/traveller/compass/camera/pictures/BurlCamera/loc69.jpg?1448639401',
        'http://www.mtocdn.ca/english/traveller/compass/camera/pictures/BurlCamera/loc70.jpg?1448639401',
        'http://www.mtocdn.ca/english/traveller/compass/camera/pictures/BurlCamera/loc76.jpg?1448639401',
        'http://www.mtocdn.ca/english/traveller/compass/camera/pictures/BurlCamera/loc77.jpg?1448639401',
        'http://www.mtocdn.ca/english/traveller/compass/camera/pictures/BurlCamera/loc74.jpg?1448639401']


def main():
    """main program - display list of images"""

    # Hardware SPI usage:
    disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

    # Initialize library.
    disp.begin(contrast=60)

    # Clear display.
    disp.clear()
    disp.display()

    while True:
        for cam in cams:
            fp = urllib2.urlopen(cam)
            file_name = cStringIO.StringIO(fp.read())
        
            image = Image.open(file_name)
            image = ImageOps.grayscale(image)
        
            rs = image.resize((84, 48))
            bw = rs.convert("1")
#            bw = rs.convert("1", dither=Image.FLOYDSTEINBERG)
        
            disp.image(bw)
            disp.display()
            time.sleep(5) # delay in seconds

# main
if "__main__" == __name__:
    main()
