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
import subprocess
import pytz
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("CYC Dashboard")
    epd = epd7in5_V2.EPD()
    
    epd.init()
    #epd.Clear()

    font54 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 54)
    #font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
    #font42 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 42)
    font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
    font30 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    #font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)

    logging.info("H: %s, W: %s", epd.height, epd.width)

    blackImage = Image.new('1', (epd.width, epd.height), 255)
    redImage = Image.new('1', (epd.width, epd.height), 255)
    drawBlack = ImageDraw.Draw(blackImage)
    drawRed = ImageDraw.Draw(redImage)
    
    # Header
    drawBlack.rectangle((0, 0, 800, 70), fill = 0)
    
    tz = pytz.timezone('America/New_York') # America/Chicago
    date_time_obj = datetime.now(tz)
    date_display = date_time_obj.strftime("%B %d, %Y") + ' '
    day_of_week = date_time_obj.strftime("%A")
    day_of_trip = 'Day 4'
    drawBlack.text((10, 20), date_display + ' | ' + day_of_week + ' | ' + day_of_trip, font = font36, fill = 1)    
    
    # Header Logo
    bmp = Image.open(os.path.join(picdir, 'cyc_logo_100x70_white_on_black.png'))
    blackImage.paste(bmp, (695, 0))

    # Content Left
    line1 = 'Welcome'
    line2 = '- Dinner is at 6pm'
    drawBlack.text((10, 80), line1, font = font54, fill = 0)    
    drawBlack.text((10, 142), line2, font = font36, fill = 0)    
   
    # Content Right
    label1 = 'Distance to Nassau' + ' '
    value1 = '80 Miles' + ' '
    drawBlack.rectangle((482, 74, 800, 164), fill = 0)
    drawBlack.text((535, 78), label1, font = font24, fill = 1)    
    drawBlack.text((570, 110), value1, font = font36, fill = 1)    

    label2 = 'Distance from Staniel Cay' + ' '
    value2 = '10 Miles' + ' '
    drawBlack.rectangle((482, 168, 800, 258), fill = 0)
    drawBlack.text((500, 172), label2, font = font24, fill = 1)    
    drawBlack.text((570, 204), value2, font = font36, fill = 1)    

    label3 = 'Location' + ' ' 
    value3 = '8.982 N, 79.519 W' + ' ' 
    drawBlack.rectangle((482, 262, 800, 352), fill = 0)
    drawBlack.text((590, 266), label3, font = font24, fill = 1)    
    drawBlack.text((515, 300), value3, font = font30, fill = 1)    
    
    # Section 5
    drawBlack.rectangle((0, 356, 158, 456), fill = 0)
    drawBlack.rectangle((162, 356, 318, 456), fill = 0)
    drawBlack.rectangle((322, 356, 478, 456), fill = 0)
    #drawBlack.rectangle((482, 356, 638, 456), fill = 0)
    drawBlack.rectangle((639, 356, 641, 456), fill = 0)
    #drawBlack.rectangle((642, 356, 800, 456), fill = 0)
    bmp = Image.open(os.path.join(picdir, '15_percent.png'))
    blackImage.paste(bmp, (642, 356))

    # Footer
    drawBlack.rectangle((0, 460, 800, 480), fill = 0)
    
    # PiSugar2 Battery Level
    # echo "get battery" | nc -q 0 127.0.0.1 8423
    battery_percentage = subprocess.check_output('echo \"get battery\" | nc -q 0 127.0.0.1 8423', shell=True, text=True)
    battery_percentage = battery_percentage.replace("battery: ", "")
    battery_percentage = "{:.1f}".format(float(battery_percentage)) + "%"
    isBatteryCharging = subprocess.check_output('echo \"get battery_charging\" | nc -q 0 127.0.0.1 8423', shell=True, text=True)
    drawBlack.text((10, 462), 'Battery: ' + battery_percentage, font = font12, fill = 1)

    # IP Address
    # /sbin/ip -o -4 addr list wlan0 | awk '{print $4}' | cut -d/ -f1
    ip_address = subprocess.check_output('ifconfig wlan0 | grep \'inet \' | awk \'{print $2}\'', shell=True, text=True)
    ip_address_display = 'IP: ' + ip_address
    drawBlack.text((164, 462), ip_address_display, font = font12, fill = 1)

    # Footer Right
    tz = pytz.timezone('America/New_York') # America/Chicago
    date_time_obj = datetime.now(tz)
    last_updated = date_time_obj.strftime("%d-%b-%Y %H:%M:%S") + ' '
    drawBlack.text((580, 462), 'Last Updated: ' + last_updated, font = font12, fill = 1)    

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
