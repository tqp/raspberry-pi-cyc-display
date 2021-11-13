#!/bin/bash

current_timestamp=$(date +"%Y-%m-%d %H:%M:%S")
sudo shutdown -c
echo "$current_timestamp: Shutdown aborted." >> /home/pi/cyc-display/cyc-display.log
