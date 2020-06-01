#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PNG Compression Size Test.

Author: Imran Matin
Email: imatin@ucsd.edu

Usage:
# in a new terminal
python test_compression_size.py

Tests the PNG compression file sizes for compression values beteween [0,9].
Inherits camera settings form the camera_config file in the directory. Captures
10 images each of a different compression size and saves them into the directory
test_compression_size. The file sizes are printed out as well. Note that the
actual image content/quality itself makes a difference for how large it is.
"""

import EasyPySpin
import cv2
import os
import shutil
from camera_config import *

IMG_DIR = "test_compression_size"
MAX_COMPRESSION = 10


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


def writeImage(cap):
    """Captures an image from 0 to MAX_COMPRESSION and writes it to disk."""
    # capture an image for each compression value
    for compression in range(0, MAX_COMPRESSION):
        ret, frame = cap.read()
        filename = os.path.join(IMG_DIR, f"compression_{compression}.png")
        cv2.imwrite(
            filename, frame, [cv2.IMWRITE_PNG_COMPRESSION, compression],
        )


def getSize():
    """Prints out the size of the image for each level of compression."""
    # print out size for each compressed image
    for compression in range(0, MAX_COMPRESSION):
        filename = os.path.join(IMG_DIR, f"compression_{compression}.png")
        size = os.path.getsize(filename) * pow(10, -6)
        size = round(size, 6)
        print(
            f"File size for PNG Compression value of {compression}: {size} megabytes."
        )


if __name__ == "__main__":
    # initialize the camera with specified settings
    cap = initializeCamera()

    print("Starting Compression Test...")

    try:
        # create new images directory each time cSBC starts up
        if os.path.exists(IMG_DIR):
            shutil.rmtree(IMG_DIR)
        os.mkdir(IMG_DIR)

        # write images to disk
        writeImage(cap)

        # get sizes of those images
        getSize()
    finally:
        # Release camera
        cap.release()
        print("Completed Compression Test...")
