#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Single image capture test.

Author: Imran Matin
Email: imatin@ucsd.edu

Usage:
# in a new terminal
python test_capture_single_image.py

Captures and displays a single image.
Inherits camera settings form the camera_config file in the directory. Captures
a single image and displays it on the screen. Press 's' to save it and 'q' to 
not.
"""

import EasyPySpin
import cv2
import os
import shutil
from camera_config import *

IMG_DIR = "test_capture_single_image"
PROMPT = "Press (s) to save the image and close the window, (q) to not save the image and close the window."


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


if __name__ == "__main__":
    # initialize the camera with specified settings
    cap = initializeCamera()

    try:
        # create new images directory each time cSBC starts up
        if os.path.exists(IMG_DIR):
            shutil.rmtree(IMG_DIR)
        os.mkdir(IMG_DIR)

        # capture an image
        ret, frame = cap.read()
        print(PROMPT)
        while True:
            # display the captured image
            cv2.imshow(filename, frame)
            key = cv2.waitKey(0)
            # save on pressing 's'
            if key == ord("s"):
                # write the image to disk
                filename = os.path.join(IMG_DIR, f"test1.png")
                cv2.imwrite(filename, frame)
                break
            # break on pressing 'q'
            if key == ord("q"):
                break
    finally:
        cv2.destroyAllWindows()
        # Release camera
        cap.release()
