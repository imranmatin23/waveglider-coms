#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Video Test.

Author: Imran Matin
Email: imatin@ucsd.edu

Usage:
# in a new terminal
python test_video.py

Opens a new video stream for the camera.
Inherits camera settings form the camera_config file in the directory. Press 's'
to capture a frame and 'q' to break the video stream.
not.
"""

import EasyPySpin
import cv2
import os
import shutil
import datetime
from camera_config import *

IMG_DIR = "test_video"
PROMPT = "Navigate to the open window. Press (s) to capture an image, (q) close the video stream."


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

    print("Starting Test...")
    try:
        # create new images directory each time cSBC starts up
        if os.path.exists(IMG_DIR):
            shutil.rmtree(IMG_DIR)
        os.mkdir(IMG_DIR)
        print(PROMPT)

        while True:
            # get an image
            ret, frame = cap.read()

            # print out metrics
            exposureTime = cap.get(cv2.CAP_PROP_EXPOSURE)
            gain = cap.get(cv2.CAP_PROP_GAIN)
            print("exposureTime:", exposureTime)
            print("gain        :", gain)
            print("\033[2A", end="")

            # display the image
            cv2.imshow("capture", frame)
            key = cv2.waitKey(0)

            # save on pressing 's'
            if key == ord("s"):
                time_stamp = datetime.datetime.now().isoformat()
                file = time_stamp + ".png"
                filename = os.path.join(IMG_DIR, file)
                cv2.imwrite(filename, frame)
                print("Saved image to > ", filename)
            # break on pressing 'q'
            if key == ord("q"):
                break
    except Exception as e:
        print("Exception occurred...")
        print(e)
    finally:
        cv2.destroyAllWindows()
        # Release camera
        cap.release()
        print("Completed Test...")
