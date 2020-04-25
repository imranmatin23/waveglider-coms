# Author: Imran Matin
# Description:

## Main libraries
# Handles multiprocessing
from multiprocessing import Process, Value
import logging

## Camera libraries
# Import deque data structure to store rolling images
from collections import deque
# Import OpenCV
import cv2
# Import calls to handle camera
import EasyPySpin
# Import os to create paths to store images at
import os

## Server libraries
# Import socket module
import socket
# Import JSON module to load dict from string
import json
# Import sys to handle exceptions
import sys


## Camera constants
# Maximum number of images in rolling buffer at once
ROLL_BUF_SIZE = 5
# Location of image directory to save images
IMG_DIR = "images"
# Type of image to save to disk
IMG_TYPE = ".png"

## Server constants
# The server's hostname or IP address
HOST = '127.0.0.1'
# The port used by the server
PORT = 65431
# number of connections that will be allowed to queue for this server
NUM_CONN = 1

# Name of file to log to 
LOG_FILE = 'logs/cSBC.log'
FILEMODE = 'w'
LOGGER_NAME = 'cSBC Logger'
MESSAGE_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Responses to client
STANDBY_RESP = b'Server set to STANDBY.'
EVENT_RESP = b'EVENT captured.'
SHUTDOWN_RESP = b'Server SHUTDOWN. Captured %d images in total.'

#### DATA TRANSFER FORMAT DEFINED HERE ####
# Define commands to be recieved from client
# STANDBY = '{"eventStatus": 0, "cameraStatus": 1}'
# EVENT = '{"eventStatus": 1, "cameraStatus": 1}'
# SHUTDOWN = '{"eventStatus": 0, "cameraStatus": 0}'
STANDBY = 'STANDBY'
EVENT = 'EVENT'
SHUTDOWN = 'SHUTDOWN'

def createLogger():
    '''Create logger for this SBC.'''
    logging.basicConfig(filename=LOG_FILE,
                        filemode=FILEMODE,
                        format=MESSAGE_FORMAT,
                        level=logging.DEBUG)
    return logging.getLogger(LOGGER_NAME)

def writeImages(rollBuf, diskImages, logger):
    '''Write images from rolling buffer to disk.'''
    try: 
        for img in rollBuf:
            # TODO: Remove to write images to disk
            # img.tofile(os.path.join(IMG_DIR, "img{}.png".format(diskImages.value)))
            diskImages.value += 1
            logger.info("Wrote image {} to disk...".format(diskImages.value))
    except:
        logger.error("Exception occurred", exc_info=True)

def captureImages(cameraStatus, eventStatus, diskImages, logger):
    '''Initialize camera and rolling buffer and recieves messages for commands. Calls function to write images.'''
    try: 
        # Create object to handle FLIR camera operations
        cap = EasyPySpin.VideoCapture(0)
        # Create rolling buffer for images
        rollBuf = deque(maxlen=ROLL_BUF_SIZE)

        while True:
            # in standby read frame, encode image, append to rolling buffer
            if (cameraStatus.value and not eventStatus.value):
                success, frame = cap.read()
                result, img = cv2.imencode(IMG_TYPE, frame)
                rollBuf.append(img)
            # write images when event triggered
            elif (cameraStatus.value and eventStatus.value):
                writeImages(rollBuf, diskImages, logger)
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

def connectionHandler(cameraStatus, eventStatus, diskImages, logger):
    '''Handles commands from mSBC and directs controls to do correct events.'''
    try:
        # open a socket for this server, bind to port and wait for connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(NUM_CONN)
            while True:
                logger.info("Waiting for connection...")
                logger.info(f"eventStatus is {eventStatus.value}. cameraStatus is {cameraStatus.value}.")

                # Establish connection with client. Waits here until client attempts to attach
                conn, addr = s.accept()

                # open the connection to the client
                with conn:
                    logger.info(f'Got connection from {addr}')
                    data = conn.recv(4096).decode('utf-8')
                    logger.info(f"Command recieved from client: {data}")

                    # Sets cSBC to STANDBY mode
                    if (data == STANDBY):
                        eventStatus.value, cameraStatus.value = False, True
                        conn.sendall(STANDBY_RESP)
                    # Triggers an event and doesn't continue function till even completed
                    elif (data == EVENT):
                        eventStatus.value, cameraStatus.value = True, True
                        while eventStatus.value:
                            continue
                        conn.sendall(EVENT_RESP)
                    # Shutsdown cSBC
                    elif (data == SHUTDOWN):
                        eventStatus.value, cameraStatus.value = False, False
                        conn.sendall(SHUTDOWN_RESP % diskImages.value)
                        break
    except:
        logger.error("Exception occurred", exc_info=True)

if __name__ == "__main__":
    '''Initalizes shared variables and Processes. Terminates camera, socket, main processes in that order.'''
    try:
        # shared variable across processes
        cameraStatus = Value('i', True)
        eventStatus = Value('i', False)
        diskImages = Value('i', 0)

        # create logger
        logger = createLogger()

        # create a process with a target function
        p1 = Process(target=connectionHandler, args=(cameraStatus, eventStatus, diskImages, logger, ))
        p2 = Process(target=captureImages, args=(cameraStatus, eventStatus, diskImages, logger, ))

        # start the process
        p1.start()
        p2.start()

        # Stops execution of current program until this process completes.    
        p2.join()
        p1.join()
    except:
        logger.error("Exception occurred", exc_info=True)