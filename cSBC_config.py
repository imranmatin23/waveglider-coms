# Author: Imran Matin
# Description: This file contains all the necessary configuration aspects for the cSBC module.

## Camera constants
# Maximum number of images in rolling buffer at once
ROLL_BUF_SIZE = 100
# Location of image directory to save images
IMG_DIR = "images"
# Type of image to save to disk
IMG_TYPE = ".png"
# Amount of time in seconds to wait after event occurs
EVENT_DELAY = 3

## Server constants
# The server's hostname or IP address
HOST = "127.0.0.1"
# The port used by the server
PORT = 65431
# number of connections that will be allowed to queue for this server
NUM_CONN = 0

# Name of file to log to
LOG_FILE = "logs/cSBC.log"
FILEMODE = "w"
LOGGER_NAME = "cSBC Logger"
MESSAGE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Responses to client
STANDBY_RESP = b"Server set to STANDBY."
EVENT_RESP = b"EVENT captured."
SHUTDOWN_RESP = b"Server SHUTDOWN. Captured %d images in total."

#### DATA TRANSFER FORMAT DEFINED HERE ####
# Define commands to be recieved from client
# STANDBY = '{"eventStatus": 0, "cameraStatus": 1}'
# EVENT = '{"eventStatus": 1, "cameraStatus": 1}'
# SHUTDOWN = '{"eventStatus": 0, "cameraStatus": 0}'
STANDBY = "STANDBY"
EVENT = "EVENT"
SHUTDOWN = "SHUTDOWN"
