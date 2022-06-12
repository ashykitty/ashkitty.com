#!/bin/bash
export TZ="/usr/share/zoneinfo/Brazil/East"
killall python3
sleep 1
python3 app.py &
