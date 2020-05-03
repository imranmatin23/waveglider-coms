#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""One line statement.

Author: Imran Matin

File is...
"""

import os
import cv2
import time
import socket
import shutil
import logging
import datetime
import EasyPySpin
import multiprocessing as mp
from collections import deque
from cSBC_config import *


def createLogger():
    """Create logger for this SBC.

    It sets the basic configuration for the logger.

    Parameters
    ----------
    param1 : int
        The first parameter.

    Returns
    -------
    logger
        Returns a logger with the specified name.

    Raises
    ------
    OSError
        list of all exceptions that are relevant to the interface.

    """
    logging.basicConfig(
        filename=LOG_FILE, filemode=FILEMODE, format=MESSAGE_FORMAT, level=logging.DEBUG
    )
    return logging.getLogger(LOGGER_NAME)


def createDatetimePath():
    dtime_str = datetime.datetime.now().isoformat().replace(":", "-").replace(".", "-")
    dtime_path = os.path.join(IMG_DIR, dtime_str)
    os.mkdir(dtime_path)
    return dtime_path


def writeImages(rollBuf, diskImages, logger):
    """Write images from rolling buffer to disk."""
    try:
        # number images in order
        num_captured = 0
        # create new dir to store images for this event
        dtime_path = createDatetimePath()
        # reverse rolling buffer to get last image captured first and write to disk
        for img in list(reversed(rollBuf)):
            img_str = f"img_{num_captured}" + IMG_TYPE
            img.tofile(os.path.join(dtime_path, img_str))
            # increment counters and log writ
            diskImages.value += 1
            num_captured += 1
            # logger.info("Wrote image {} to disk...".format(diskImages.value))
        return num_captured
    except:
        logger.error("Exception occurred", exc_info=True)


# DEBUG
def captureImages(cameraStatus, eventStatus, diskImages, logger, testEventFlag):
    """Initialize camera and rolling buffer and recieves messages for commands. Calls function to write images."""
    try:
        # Create object to handle FLIR camera operations
        cap = EasyPySpin.VideoCapture(0)
        # Create rolling buffer for images
        rollBuf = deque(maxlen=ROLL_BUF_SIZE)

        # DEBUG
        img_counter = 0

        while True:
            # in standby read frame, encode image, append to rolling buffer
            if cameraStatus.value and not eventStatus.value:
                success, frame = cap.read()
                result, img = cv2.imencode(IMG_TYPE, frame)
                rollBuf.append(img)

                # DEBUG
                if testEventFlag.value:
                    img_counter += 1

            # write images when event triggered
            elif cameraStatus.value and eventStatus.value:
                # DEBUG
                print(
                    f"Number of images captured after {EVENT_DELAY} sec delay: {img_counter}."
                )
                img_counter = 0

                # DEBUG
                start = time.time()

                num_captured = writeImages(rollBuf, diskImages, logger)

                # DEBUG
                elapsed = time.time() - start
                print(
                    f"writeImages captured {num_captured} images in {elapsed} seconds."
                )

                rollBuf.clear()
                eventStatus.value = False
            # release the camera and exit
            else:
                break
    except:
        logger.error("Exception occurred", exc_info=True)
    # release the camera and exit
    finally:
        cap.release()
        logger.info("Successflly released camera...")


# DEBUG
def connectionHandler(cameraStatus, eventStatus, diskImages, logger, testEventFlag):
    """Handles commands from mSBC and directs controls to do correct events."""
    try:
        while True:
            # open a socket for this server, bind to port and wait for connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST, PORT))
                s.listen(NUM_CONN)

                print("\n\nWaiting for connection...")

                # Establish connection with client. Closes socket to disallow for more connections
                conn, addr = s.accept()
                s.close()

                # DEBUG
                curr_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
                print(f"Connection accepted at time {curr_time} seconds")
                print("-------------------------------------------------")

                # open the connection to the client
                with conn:
                    data = conn.recv(4096).decode("utf-8")

                    # Sets cSBC to STANDBY mode
                    if data == STANDBY:
                        eventStatus.value, cameraStatus.value = False, True
                        conn.sendall(STANDBY_RESP)
                    # Triggers an event and doesn't continue function till even completed
                    elif data == EVENT:

                        # DEBUG
                        testEventFlag.value = True

                        # Wait for time for full event to complete
                        time.sleep(EVENT_DELAY)

                        # DEBUG
                        testEventFlag.value = False

                        # TODO: Are the while loop and send all necessary?
                        eventStatus.value, cameraStatus.value = True, True
                        while eventStatus.value:
                            continue
                        conn.sendall(EVENT_RESP)
                    # Shutsdown cSBC
                    elif data == SHUTDOWN:
                        eventStatus.value, cameraStatus.value = False, False
                        conn.sendall(SHUTDOWN_RESP % diskImages.value)
                        break
    except:
        logger.error("Exception occurred", exc_info=True)


if __name__ == "__main__":
    """Initalizes shared variables and Processes. Terminates camera, socket, main processes in that order."""
    try:
        # shared variable across processes
        cameraStatus = mp.Value("i", True)
        eventStatus = mp.Value("i", False)
        diskImages = mp.Value("i", 0)

        # DEBUG
        testEventFlag = mp.Value("i", False)

        # create logger
        logger = createLogger()

        # create new images directory each time cSBC starts up
        if os.path.exists(IMG_DIR):
            shutil.rmtree(IMG_DIR)
        os.mkdir(IMG_DIR)

        # DEBUG
        # create a process with a target function
        p1 = mp.Process(
            target=connectionHandler,
            args=(cameraStatus, eventStatus, diskImages, logger, testEventFlag,),
        )
        # DEBUG
        p2 = mp.Process(
            target=captureImages,
            args=(cameraStatus, eventStatus, diskImages, logger, testEventFlag,),
        )

        # start the process
        p1.start()
        p2.start()

        # Stops execution of current program until this process completes.
        p2.join()
        p1.join()
    except:
        logger.error("Exception occurred", exc_info=True)