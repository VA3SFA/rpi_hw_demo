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
from datetime import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import socket
import fcntl
import struct
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

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

FONT_SIZE = 10


def main():
    """main program - draw and display a test image"""

    now = datetime.today()
    # Hardware SPI usage:
    disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

    # Initialize library.
    disp.begin(contrast=60)
    
    # Clear display.
    disp.clear()
    disp.display()


    # initially set all white background
    image = Image.new('1', (84,48), WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)
    width, height = image.size

#    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)
    font = ImageFont.load_default()

    ethaddr = get_ip_address('eth0')


    draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
    draw.text((0, 0), '{c:s}'.format(c=ethaddr), fill=BLACK, font=font)
    draw.text((5, 10), '{h:02d}:{m:02d}:{s:02d}'.format(h=now.hour, m=now.minute, s=now.second), fill=BLACK, font=font)


    # Display image.
    disp.image(image)
    disp.display()
    

# main
if "__main__" == __name__:
    main()
