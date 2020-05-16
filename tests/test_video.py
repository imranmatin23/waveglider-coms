# Author: Imran Matin
# Description: Provides realtime video output for the camera.

import EasyPySpin
import cv2
import os
import shutil
from camera_config import *


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
        while True:
            # get an image
            ret, frame = cap.read()

            # print out metrics
            exposureTime = cap.get(cv2.CAP_PROP_EXPOSURE)
            gain = cap.get(cv2.CAP_PROP_GAIN)
            print("exposureTime:", exposureTime)
            print("gain        :", gain)
            print("\033[2A", end="")

            # resize the image
            # img_show = cv2.resize(frame, None, fx=args.scale, fy=args.scale)

            # display the image
            cv2.imshow("capture", frame)

            # check if q key pressed to quit
            key = cv2.waitKey(30)
            if key == ord("q"):
                break
            # elif key==ord("c"):
            #     import datetime
            #     time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            #     filepath = time_stamp + ".png"
            #     cv2.imwrite(filepath, frame)
            #     print("Export > ", filepath)
    finally:
        cv2.destroyAllWindows()
        # Release camera
        cap.release()
