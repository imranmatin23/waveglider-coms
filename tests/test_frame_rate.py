#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Frame Rate Test.

Author: Imran Matin
Email: imatin@ucsd.edu

Source Code: https://www.learnopencv.com/how-to-find-frame-rate-or-frames-per-second-fps-in-opencv-python-cpp/

Usage:
# in a new terminal
python test_frame_rate.py


Tests how long it takes to capture NUM_IMAGES with the FPS specified.
Inherits camera settings from the camera_config file in the directory. 
Imports the NUM_FRAMES to capture from the camera_config file in the directory.
Captures NUM_FRAMES and uses the time taken to do so to calculate actual FPS.
"""

import EasyPySpin
import cv2
import time
from camera_config import *

NUM_FRAMES = 120


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


def getCurrentFPS(cap):
    """Prints the current FPS for this camera."""
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split(".")

    if int(major_ver) < 3:
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        print(f"Frames per second using cap.get(cv2.cv.CV_CAP_PROP_FPS): {fps}")
    else:
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Frames per second using cap.get(cv2.CAP_PROP_FPS) : {fps}")


def calculateFPS(cap):
    """Calculates the true FPS for this camera."""
    # Start time
    start = time.time()

    # Grab NUM_FRAMES
    for i in range(0, NUM_FRAMES):
        ret, frame = cap.read()

    # End time
    end = time.time()

    # Time elapsed
    seconds = end - start
    print(f"Time taken : {seconds} seconds")

    # Calculate frames per second
    fps = NUM_FRAMES / seconds
    print(f"Estimated frames per second : {fps}")


if __name__ == "__main__":
    # initialize the camera with specified settings
    cap = initializeCamera()

    try:
        print("Starting Frame Rate Test...")
        # print current FPS
        getCurrentFPS(cap)

        print(f"Capturing {NUM_FRAMES} frames.")

        # print true FPS
        calculateFPS(cap)

    finally:
        # Release video
        cap.release()
        print("Completed Frame Rate Test...")
