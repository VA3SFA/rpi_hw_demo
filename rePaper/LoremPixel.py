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
from EPD import EPD

cam = 'http://lorempixel.com/400/200'

def main():
    """main program - display list of images"""

    epd = EPD()

    epd.clear()

    print('panel = {p:s} {w:d} x {h:d}  version={v:s} COG={g:d} FILM={f:d}'.format(p=epd.panel, w=epd.width, h=epd.height, v=epd.version, g=epd.cog, f=epd.film))


    while True:
        fp = urllib2.urlopen(cam)
        file_name = cStringIO.StringIO(fp.read())
    
        image = Image.open(file_name)
        image = ImageOps.grayscale(image)
    
        rs = image.resize((epd.width, epd.height))
        bw = rs.convert("1", dither=Image.FLOYDSTEINBERG)
    
        epd.display(bw)
        epd.update()
        time.sleep(5) # delay in seconds

# main
if "__main__" == __name__:
    main()
