#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import pytz
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("CYC Dashboard")
    epd = epd7in5_V2.EPD()
    
    epd.init()
    #epd.Clear()

    font54 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 54)
    font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
    font42 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 42)
    font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
    font30 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)

    logging.info("H: %s, W: %s", epd.height, epd.width)

    blackImage = Image.new('1', (epd.width, epd.height), 255)
    redImage = Image.new('1', (epd.width, epd.height), 255)
    drawBlack = ImageDraw.Draw(blackImage)
    drawRed = ImageDraw.Draw(redImage)
    
    # Header
    drawBlack.rectangle((0, 0, 800, 70), fill = 0)
    date = 'November 11, 2021'

    drawBlack.text((10, 20), 'November 11, 2021 | Thursday | Day 4', font = font36, fill = 1)    

    # Content Left
    drawBlack.text((10, 100), 'Welcome', font = font54, fill = 0)    
    

    # Footer
    drawBlack.rectangle((0, 460, 800, 480), fill = 0)
    tz = pytz.timezone('America/New_York') # America/Chicago
    date_time_obj = datetime.now(tz)
    last_updated = date_time_obj.strftime("%d-%b-%Y %H:%M:%S") + ' '
    drawBlack.text((570, 462), 'Last Updated: ' + last_updated, font = font12, fill = 1)    

    #drawRed.rectangle((10, 150, 60, 200), fill = 0)
    #draw_Himage.text((2, 0), 'hello world', font = font18, fill = 0)
    #draw_Himage.text((2, 20), '7.5inch epd', font = font18, fill = 0)
    #draw_Himage_Other.text((20, 50), u'微雪电子', font = font18, fill = 0)
    #draw_Himage_Other.line((10, 90, 60, 140), fill = 0)
    #draw_Himage_Other.line((60, 90, 10, 140), fill = 0)
    #draw_Himage_Other.rectangle((10, 90, 60, 140), outline = 0)
    #draw_Himage_Other.line((95, 90, 95, 140), fill = 0)
    #draw_Himage.line((70, 115, 120, 115), fill = 0)
    #draw_Himage.arc((70, 90, 120, 140), 0, 360, fill = 0)
    #draw_Himage.chord((70, 150, 120, 200), 0, 360, fill = 0)
  
    logging.info("Drawing...")  
    epd.display(epd.getbuffer(blackImage))
    #epd.display(epd.getbuffer(blackImage), epd.getbuffer(redImage))

    logging.info("Time to sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
