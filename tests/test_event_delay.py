#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Event Delay Test.

Author: Imran Matin
Email: imatin@ucsd.edu

Usage:
# in a new terminal
python test_event_delay.py

Tests the average number of images captured for each delay value [0,MAX_DELAY].
Inherits camera settings form the camera_config file in the directory. Captures
images for NUM_TRIALS for each delay value between [0, MAX_DELAY]. Takes the 
average of all NUM_TRIALS for each delay value and prints it out.
"""

import EasyPySpin
import cv2
import time
from collections import deque
import numpy as np
from camera_config import *

IMG_TYPE = ".png"
NUM_TRIALS = 10
MAX_DELAY = 3
BUF_SIZE = 150
PROMPT = f"The number of images captured after an event delay is the average number of images captured accross {NUM_TRIALS} trials."


def initializeCamera():
    """Initializes camera object with the correct settings."""
    cap = EasyPySpin.VideoCapture(0)

    cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
    cap.set(cv2.CAP_PROP_GAIN, GAIN)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, BRIGHTNESS)
    cap.set(cv2.CAP_PROP_GAMMA, GAMMA)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    cap.set(cv2.CAP_PROP_BACKLIGHT, BACKLIGHT)

    return cap


def calcNumCaptured(cap, delay):
    """Captures as many images into rollBuf for delay number of seconds."""
    # Create rolling buffer for images
    rollBuf = deque(maxlen=BUF_SIZE)

    # start time
    startTime = time.time()

    # capture an image for delay seconds
    while time.time() - startTime < delay:
        ret, frame = cap.read()
        result, img = cv2.imencode(IMG_TYPE, frame)
        rollBuf.append(img)

    # return the number of images captured in this delay
    return len(rollBuf)


if __name__ == "__main__":
    # initialize the camera with specified settings
    cap = initializeCamera()

    try:
        print("Starting Event Delay Test...")
        print(PROMPT)
        # Test possible delay values
        for delay in range(0, MAX_DELAY):
            # list to store number of images captured for this delay
            num_captured = []
            # execute number of trials for this delay value
            for i in range(0, NUM_TRIALS):
                # append the number of images captured during delay seconds for this trial
                num_captured.append(calcNumCaptured(cap, delay))

            # print the average of all trials for this delay value
            print(
                f"An event delay of {delay} seconds captures {np.average(num_captured)} images."
            )
    finally:
        # Release camera
        cap.release()
        print("Completed Event Delay Test...")
