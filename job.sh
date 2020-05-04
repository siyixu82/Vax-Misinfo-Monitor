#!/bin/sh
cd "$(dirname "$0")";
CWD="$(pwd)"
echo $CWD
/home/vcm/.pyenv/shims/python3.7 /home/vcm/TwitterMonitor/TwitterMonitor_3.py
