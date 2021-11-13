#!/bin/bash

set -e

echo "Running update-and-schedule.sh" >> log.txt 

WAKEUP_AFTER=600
echo "WAKEUP_AFTER: $WAKEUP_AFTER"

rtc_time=$(echo "get rtc_time" | nc -q 0 127.0.0.1 8423)
echo "rtc_time      : " + $rtc_time

rtc_alarm_time=$(echo "get rtc_alarm_time" | nc -q 0 127.0.0.1 8423)
echo "rtc_alarm_time: " + $rtc_alarm_time

ready_for_shutdown=false

if [[ x"$rtc_time" =~ "rtc_time:" ]]; then
    rtc_time=${rtc_time#*" "}
    echo "rtc_time   : $rtc_time"

    # Set next wakeup time
    wakeup_time=$(date -d $rtc_time +%s)
    echo "wakeup_time1: $wakeup_time"
    wakeup_time=$(($wakeup_time + $WAKEUP_AFTER));
    echo "wakeup_time2: $wakeup_time"
    wakeup_time=$(date -d @$wakeup_time --iso-8601=seconds)
    echo "wakeup_time3: $wakeup_time"

    r=$(echo "rtc_alarm_set ${wakeup_time} 127" | nc -q 0 127.0.0.1 8423)
    echo "r: $r"

    if [[ x"$r" =~ "done" ]]; then
        echo "Ready for shutdown."
        rtc_alarm_time_new=$(echo "get rtc_alarm_time" | nc -q 0 127.0.0.1 8423)
        echo "New Alarm Time: $rtc_alarm_time_new"
        ready_for_shutdown=true
    else
        echo "Error: Could not set RTC wakeup time."
        exit 1
    fi
else
    echo "Error: Could not get RTC."
    exit 1
fi

# Refresh Display
echo "Refresh Display"
/usr/bin/python3 /home/pi/cyc-display/refresh-dashboard.py

# Sleep for 30 seconds to allow for logon.
echo "Initiating shutdown in 30 seconds..."
sleep 30

if [ $ready_for_shutdown ]; then
    echo "Scheduling shutdown in one minute..."
    #sudo shutdown -h +1 "Shutting down in one minute."
else
    echo "Error: Could not set RTC wakeup time."
    exit 1
fi
