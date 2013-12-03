#!/usr/bin/env bash

python checktoday.py >> log 2>&1 &

python serverstatus.py &
