# Author: Imran Matin
# Description: Captures and displays a single image.

import EasyPySpin
import cv2
import os
import shutil
from camera_config import *

IMG_DIR = "test_capture_single_image"


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

        filename = os.path.join(IMG_DIR, f"test1.png")

        ret, frame = cap.read()
        while True:
            cv2.imshow(filename, frame)  # display the captured image
            if cv2.waitKey(1) & 0xFF == ord("y"):  # save on pressing 'y'
                cv2.imwrite(filename, frame)
                break
    finally:
        cv2.destroyAllWindows()
        # Release camera
        cap.release()
