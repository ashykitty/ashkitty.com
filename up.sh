#!/bin/bash
export TZ="/usr/share/zoneinfo/Brazil/East"
killall python3
if [ $# -eq 0 ]; then
	python3 -m uvicorn app:app --port 6969 --host 0.0.0.0 --reload --log-level critical &
else
	if [ $1 == "debug" ]; then
		python3 -m uvicorn app:app --port 6969 --host 0.0.0.0 --reload &
	fi
fi
