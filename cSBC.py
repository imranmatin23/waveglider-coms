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
        filename=LOG_FILE,
        filemode=FILEMODE,
        format=MESSAGE_FORMAT,
        datefmt=DATE_FORMAT,
        level=logging.DEBUG,
    )
    return logging.getLogger(LOGGER_NAME)


def createDatetimePath():
    dtime_str = datetime.datetime.now().isoformat()
    dtime_path = os.path.join(IMG_DIR, dtime_str)
    os.mkdir(dtime_path)
    return dtime_path


def logCameraProperties(cap, logger):
    """Logs the current camera properties."""
    logger.debug(f"Camera Exposure: {cap.get(cv2.CAP_PROP_EXPOSURE)}")
    logger.debug(f"Camera Gain: {cap.get(cv2.CAP_PROP_GAIN)}")
    logger.debug(f"Camera Brightness: {cap.get(cv2.CAP_PROP_BRIGHTNESS)}")
    logger.debug(f"Camera Gamma: {cap.get(cv2.CAP_PROP_GAMMA)}")
    logger.debug(f"Camera FPS: {cap.get(cv2.CAP_PROP_FPS)}")
    logger.debug(f"Camera Backlight: {cap.get(cv2.CAP_PROP_BACKLIGHT)}")
    logger.debug(f"Camera Frame Width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
    logger.debug(f"Camera Frame Height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
    logger.debug(f"Camera Temperature: {cap.get(cv2.CAP_PROP_TEMPERATURE)}")


def initalizeCamera(logger):
    """Initalizes camera object with the correct settings."""
    cap = EasyPySpin.VideoCapture(0)
    logger.debug(f"Created {cap}")

    cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
    cap.set(cv2.CAP_PROP_GAIN, GAIN)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, BRIGHTNESS)
    cap.set(cv2.CAP_PROP_GAMMA, GAMMA)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    cap.set(cv2.CAP_PROP_BACKLIGHT, BACKLIGHT)

    logCameraProperties(cap, logger)
    return cap


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
            # increment counters and log write
            diskImages.value += 1
            num_captured += 1
        logger.debug(f"Wrote {num_captured} images to disk at {dtime_path}.")
        return num_captured
    except:
        logger.error("Exception occurred", exc_info=True)


def captureImages(cameraStatus, eventStatus, diskImages, logger):
    """Initialize camera and rolling buffer and recieves messages for commands. Calls function to write images."""
    try:
        # Create object to handle FLIR camera operations
        cap = initalizeCamera(logger)

        # Create rolling buffer for images
        rollBuf = deque(maxlen=ROLL_BUF_SIZE)
        logger.debug(f"Created {rollBuf}")

        logger.debug(f"Capturing images.")
        while True:
            # in standby read frame, encode image, append to rolling buffer
            if cameraStatus.value and not eventStatus.value:
                success, frame = cap.read()
                result, img = cv2.imencode(IMG_TYPE, frame)
                rollBuf.append(img)
            # write images when event triggered
            elif cameraStatus.value and eventStatus.value:
                logger.debug(f"Writing images to disk.")
                num_captured = writeImages(rollBuf, diskImages, logger)
                rollBuf.clear()
                logger.debug(f"Cleared rolling buffer.")
                eventStatus.value = False
            # release the camera and exit
            else:
                break
    except:
        logger.error("Exception occurred", exc_info=True)
    # release the camera and exit
    finally:
        cap.release()
        logger.info("Successfully released camera.")


def performCommand(conn, cameraStatus, eventStatus, diskImages, logger):
    """Handle command."""
    try:
        # open the connection to the client
        with conn:
            data = conn.recv(4096).decode("utf-8")
            logger.debug(f"Recieved {data}.")

            # get uptime of the system
            if data == UPTIME:
                uptime = round(time.time() - startTime, 6)
                conn.sendall(UPTIME_RESP % uptime)
                logger.debug(f"The current uptime is {uptime} seconds.")

            # Triggers an event and doesn't continue function till even completed
            elif data == EVENT:
                # Wait for time for full event to complete
                time.sleep(EVENT_DELAY)
                eventStatus.value, cameraStatus.value = True, True
                while eventStatus.value:
                    continue
                conn.sendall(EVENT_RESP)

            # Shutsdown cSBC
            elif data == SHUTDOWN:
                eventStatus.value, cameraStatus.value = False, False
                conn.sendall(SHUTDOWN_RESP % diskImages.value)
                return True

        return False
    except:
        logger.error("Exception occurred", exc_info=True)


def connectionHandler(cameraStatus, eventStatus, diskImages, logger):
    """Handles commands from mSBC and directs controls to do correct events."""
    try:
        while True:
            # open a socket for this server, bind to port and wait for connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST, PORT))
                s.listen(NUM_CONN)
                logger.debug(f"Bound to {HOST}-{PORT} and listening.")

                # Establish connection with client. Closes socket to disallow for more connections
                conn, addr = s.accept()
                s.close()
                logger.debug(
                    f"Acccepted connection from {conn}-{addr} and closed server socket."
                )

                # handle connection and break if shutdown recieved
                if performCommand(conn, cameraStatus, eventStatus, diskImages, logger):
                    break

    except:
        logger.error("Exception occurred", exc_info=True)


if __name__ == "__main__":
    """Initalizes shared variables and Processes. Terminates camera, socket, main processes in that order."""
    try:
        # track start time
        global startTime
        startTime = time.time()

        # shared variable across processes
        cameraStatus = mp.Value("i", True)
        eventStatus = mp.Value("i", False)
        diskImages = mp.Value("i", 0)

        # create logger
        logger = createLogger()
        logger.debug(f"Logger created for {__file__}.")

        # create new images directory each time cSBC starts up
        if os.path.exists(IMG_DIR):
            shutil.rmtree(IMG_DIR)
        os.mkdir(IMG_DIR)
        logger.debug(f"New image directory created at {IMG_DIR}.")

        # create a process with a target function
        p1 = mp.Process(
            target=connectionHandler,
            args=(cameraStatus, eventStatus, diskImages, logger,),
        )
        p2 = mp.Process(
            target=captureImages, args=(cameraStatus, eventStatus, diskImages, logger,)
        )

        # start the process
        p1.start()
        logger.debug(f"{p1}.")
        p2.start()
        logger.debug(f"{p2}.")

        # Stops execution of current program until this process completes.
        p2.join()
        logger.debug(f"{p2}.")
        p1.join()
        logger.debug(f"{p1}.")
    except:
        logger.error("Exception occurred", exc_info=True)
