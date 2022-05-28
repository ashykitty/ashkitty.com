#!/bin/bash    
python3 -m uvicorn app:app --port 6969 --host 0.0.0.0 --reload --log-config "logs/log.ini" &
