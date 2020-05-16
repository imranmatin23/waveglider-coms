#!/bin/bash

# Turn of DSI-1 LP internal display
xrandr --output DSI-1 --off

# activate cond environment
. ~/anaconda3/etc/profile.d/conda.sh
conda activate spinnaker_py37

# enter script directory and run
cd /home/imran/Desktop/waveglider-coms
python cSBC.py
