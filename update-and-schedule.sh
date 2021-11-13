#!/bin/bash

echo "Running update-and-schedule.sh" >> log.txt 

echo "Refresh Display"
python3 ./refresh-dashboard.py

rtc_time=$(echo "get rtc_time" | nc -q 0 127.0.0.1 8423)
echo "rtc_time      : " + $rtc_time

rtc_alarm_time=$(echo "get rtc_alarm_time" | nc -q 0 127.0.0.1 8423)
echo "rtc_alarm_time: " + $rtc_alarm_time

SHUTDOWN_AFTER=60
echo "SHUTDOWN_AFTER: $SHUTDOWN_AFTER"
WAKEUP_AFTER=3600 
echo "WAKEUP_AFTER: $WAKEUP_AFTER"

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
        #echo "Sleeping for $SHUTDOWN_AFTER seconds before shutting down."
        # Sleep for n seconds then poweroff
        #sleep $SHUTDOWN_AFTER
        sudo shutdown -h +2 "Shutting down in two minutes."
    else
        echo "Error: Could not set RTC wakeup time."
        exit 1
    fi
else
    echo "Error: Could not get RTC."
    exit 1
fi


