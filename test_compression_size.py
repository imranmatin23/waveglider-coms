# Author: Imran Matin
# Description: PNG Compression Size Test. Test compression of PNG images at all compression levels.

import EasyPySpin
import cv2
import os
import shutil

IMG_DIR = "test_compression_size"
# Camera Settings
EXPOSURE = 5000
GAIN = 2
BRIGHTNESS = 1
GAMMA = 0.25
FPS = 8
BACKLIGHT = 1


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

    # create new images directory each time cSBC starts up
    if os.path.exists(IMG_DIR):
        shutil.rmtree(IMG_DIR)
    os.mkdir(IMG_DIR)

    # capture an image for each compression value
    for compression in range(0, 10):
        ret, frame = cap.read()
        filename = os.path.join(IMG_DIR, f"compression_{compression}.png")
        cv2.imwrite(
            filename, frame, [cv2.IMWRITE_PNG_COMPRESSION, compression],
        )

    # print out size for each compressed image
    for compression in range(0, 10):
        filename = os.path.join(IMG_DIR, f"compression_{compression}.png")
        size = os.path.getsize(filename) * pow(10, -6)
        size = round(size, 6)
        print(
            f"File size for PNG Compression value of {compression}: {size} megabytes."
        )

    # Release camera
    cap.release()
