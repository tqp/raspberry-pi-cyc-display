#!/bin/bash

timestamp=$(date +'%Y-%m-%d %H:%M:%S')
echo $timestamp
echo $timestamp >> /home/pi/cyc-display/log_test1.txt
