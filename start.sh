#!/bin/bash
export TZ="/usr/share/zoneinfo/Brazil/East"
python3 -m uvicorn app:app --port 6969 --host 0.0.0.0 --reload --log-level critical &
