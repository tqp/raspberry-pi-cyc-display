#!/bin/bash

current_timestamp=$(date +"%Y-%m-%d %H:%M:%S")
echo "$current_timestamp: double button press" >> /home/pi/cyc-display/cyc-display.log
sh /home/pi/cyc-display/shutdown-abort.sh
