#!/bin/bash

date -d @`cat /run/systemd/shutdown/scheduled | head -n 1 | cut -c6-15`
