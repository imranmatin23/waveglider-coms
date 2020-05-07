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

if __name__ == "__main__":
    cap = EasyPySpin.VideoCapture(0)

    # set FPS
    cap.set(cv2.CAP_PROP_FPS, FPS)

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split(".")

    if int(major_ver) < 3:
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        print(f"Frames per second using cap.get(cv2.cv.CV_CAP_PROP_FPS): {fps}")
    else:
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Frames per second using cap.get(cv2.CAP_PROP_FPS) : {fps}")

    print(f"Capturing {NUM_FRAMES} frames.")

    # Start time
    start = time.time()

    # Grab a few frames
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

    # Release video
    cap.release()
