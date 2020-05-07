# Author: Imran Matin
# Description: PNG Compression Size Test. Test compression of PNG images at all compression levels.

import EasyPySpin
import cv2
import time
from collections import deque
import numpy as np
import os
import shutil

# Camera Settings
EXPOSURE = 5000
GAIN = 2
BRIGHTNESS = 1
GAMMA = 0.25
FPS = 8
BACKLIGHT = 1

# buffer size
BUF_SIZE = 150
# image type
IMG_TYPE = ".png"
# test img dir
IMG_DIR = "test_write_speed"


def initalizeCamera():
    """Initalizes camera object with the correct settings."""
    cap = EasyPySpin.VideoCapture(0)

    cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
    cap.set(cv2.CAP_PROP_GAIN, GAIN)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, BRIGHTNESS)
    cap.set(cv2.CAP_PROP_GAMMA, GAMMA)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    cap.set(cv2.CAP_PROP_BACKLIGHT, BACKLIGHT)

    return cap


if __name__ == "__main__":
    # initalize the camera with specified settings
    cap = initalizeCamera()
    try:
        # create new images directory each time cSBC starts up
        if os.path.exists(IMG_DIR):
            shutil.rmtree(IMG_DIR)
        os.mkdir(IMG_DIR)

        # Create rolling buffer for images
        rollBuf = deque(maxlen=BUF_SIZE)

        # store each write time
        times = []

        for i in range(0, 5):

            # capture an image for each compression value
            while len(rollBuf) != BUF_SIZE:
                ret, frame = cap.read()
                result, img = cv2.imencode(IMG_TYPE, frame)
                rollBuf.append(img)

            print(f"Collected {BUF_SIZE} images...")

            # start time
            startTime = time.time()

            # write images to disk
            for i, img in enumerate(list(reversed(rollBuf))):
                img_str = f"img_{i}" + IMG_TYPE
                img.tofile(os.path.join(IMG_DIR, img_str))

            # get time elapsed
            timeElapsed = time.time() - startTime
            print(
                f"It took {timeElapsed} seconds to write {len(rollBuf)} images to disk."
            )
            times.append(timeElapsed)

            # clear rollBuf
            rollBuf.clear()

        print(
            f"For {5} writes, it took {np.average(times)} seconds to write {BUF_SIZE} images to disk on average."
        )
    finally:
        # Release camera
        cap.release()
