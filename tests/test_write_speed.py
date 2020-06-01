#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Write Speed Test.

Author: Imran Matin
Email: imatin@ucsd.edu

Usage:
# in a new terminal
python test_write_speed.py

Tests the average write speed for writing BUF_SIZE images from the rolling
buffer into disk for NUM_WRITES trails.
Inherits camera settings form the camera_config file in the directory.
"""

import EasyPySpin
import cv2
import time
from collections import deque
import numpy as np
import os
import shutil
from camera_config import *

IMG_TYPE = ".png"
IMG_DIR = "test_write_speed"
BUF_SIZE = 150
NUM_WRITES = 3


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


def collectImages(rollBuf):
    """Collects BUF_SIZE images into the rollBuf."""
    # capture an image for each compression value
    while len(rollBuf) != BUF_SIZE:
        ret, frame = cap.read()
        result, img = cv2.imencode(IMG_TYPE, frame)
        rollBuf.append(img)

    print(f"Collected {BUF_SIZE} images...")
    return rollBuf


def timeWrite(times, rollBuf):
    """Calculates time required to write the rollBuf images to disk."""
    # start time
    startTime = time.time()

    # write images to disk
    for i, img in enumerate(list(reversed(rollBuf))):
        img_str = f"img_{i}" + IMG_TYPE
        img.tofile(os.path.join(IMG_DIR, img_str))

    # get time elapsed
    timeElapsed = time.time() - startTime
    print(f"It took {timeElapsed} seconds to write {len(rollBuf)} images to disk.")
    times.append(timeElapsed)

    # clear rollBuf
    rollBuf.clear()

    return times, rollBuf


if __name__ == "__main__":
    # initialize the camera with specified settings
    cap = initializeCamera()
    # Create rolling buffer for images
    rollBuf = deque(maxlen=BUF_SIZE)
    # list store how long it took for each write
    times = []

    try:
        print("Starting Write Speed Test...")
        # create new images directory each time cSBC starts up
        if os.path.exists(IMG_DIR):
            shutil.rmtree(IMG_DIR)
        os.mkdir(IMG_DIR)

        # time the write time for NUM_WRITES
        for i in range(0, NUM_WRITES):
            # collect BUF_SIZE number of images and time their write to disk
            rollBuf = collectImages(rollBuf)
            times, rollBuf = timeWrite(times, rollBuf)

        print(
            f"For {NUM_WRITES} writes, it took {np.average(times)} seconds to write {BUF_SIZE} images to disk on average."
        )
    finally:
        # Release camera
        cap.release()
        print("Completed Write Speed Test...")
