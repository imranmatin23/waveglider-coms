# Author: Imran Matin
# Description: Frame Rate Test. Set FPS at beginning and test how long it takes to canpture NUM_IMAGES.
# Source Code: https://www.learnopencv.com/how-to-find-frame-rate-or-frames-per-second-fps-in-opencv-python-cpp/

import EasyPySpin
import cv2
import time

# Range for FPS [1,8.57]
FPS = 8
# Number of frames to capture
NUM_FRAMES = 120

# Author: Imran Matin
# Description: PNG Compression Size Test. Test compression of PNG images at all compression levels.

import EasyPySpin
import cv2
import os
import shutil
import PySpin

# Camera Settings
EXPOSURE = 100
GAIN = 2
BRIGHTNESS = 1
GAMMA = 0.25
FPS = 25
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
    try:
        print(cap)
        # PS0FrameRateActual_node = PySpin.CFloatPtr(
        #     nodemap.GetNode("PS0FrameRateActual")
        # )
        # PS0FrameRateActual = PS0FrameRateActual_node.GetValue()
        # print(PS0FrameRateActual)

    #     # set FPS
    #     cap.set(cv2.CAP_PROP_FPS, FPS)

    #     # Find OpenCV version
    #     (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split(".")

    #     if int(major_ver) < 3:
    #         fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    #         print(f"Frames per second using cap.get(cv2.cv.CV_CAP_PROP_FPS): {fps}")
    #     else:
    #         fps = cap.get(cv2.CAP_PROP_FPS)
    #         print(f"Frames per second using cap.get(cv2.CAP_PROP_FPS) : {fps}")

    #     print(f"Capturing {NUM_FRAMES} frames.")

    #     # Start time
    #     start = time.time()

    #     # Grab a few frames
    #     for i in range(0, NUM_FRAMES):
    #         ret, frame = cap.read()

    #     # End time
    #     end = time.time()

    #     # Time elapsed
    #     seconds = end - start
    #     print(f"Time taken : {seconds} seconds")

    #     # Calculate frames per second
    #     fps = NUM_FRAMES / seconds
    #     print(f"Estimated frames per second : {fps}")
    finally:
        # Release video
        cap.release()
