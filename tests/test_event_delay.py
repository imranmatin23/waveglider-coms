# Author: Imran Matin
# Description: PNG Compression Size Test. Test compression of PNG images at all compression levels.

import EasyPySpin
import cv2
import time
from collections import deque
import numpy as np

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

        print(
            f"The number of images captured after an event delay is the average number of images captured accross {10} trials."
        )

        # Test possible delay values
        for delay in range(0, 6):
            # list to store number of images captured
            num_captured = []

            for i in range(0, 10):
                # Create rolling buffer for images
                rollBuf = deque(maxlen=BUF_SIZE)

                # start time
                startTime = time.time()

                # capture an image for each compression value
                while time.time() - startTime < delay:
                    ret, frame = cap.read()
                    result, img = cv2.imencode(IMG_TYPE, frame)
                    rollBuf.append(img)

                num_captured.append(len(rollBuf))

            print(
                f"An event delay of {delay} seconds captures {np.average(num_captured)} images."
            )
    finally:
        # Release camera
        cap.release()
