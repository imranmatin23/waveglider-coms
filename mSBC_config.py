# Author: Imran Matin
# Description: This file contains all the necessary configuration aspects for the mSBC module.

# The server's hostname or IP address
HOST = "127.0.0.1"
# The port used by the server
PORT = 65431
# Name of file to log to
LOG_FILE = "logs/mSBC.log"
FILEMODE = "w"
LOGGER_NAME = "mSBC Logger"
MESSAGE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# User strings
PROMPT = "What command would you like to send? [0:standby,1:event,2:shutdown]: "

#### DATA TRANSFER FORMAT DEFINED HERE ####
# define user choices
STANDBY = "0"
EVENT = "1"
SHUTDOWN = "2"
# COMMANDS = {
#     STANDBY: b'{"eventStatus": 0, "cameraStatus": 1}',
#     EVENT: b'{"eventStatus": 1, "cameraStatus": 1}',
#     SHUTDOWN: b'{"eventStatus": 0, "cameraStatus": 0}'
# }
COMMANDS = {STANDBY: b"STANDBY", EVENT: b"EVENT", SHUTDOWN: b"SHUTDOWN"}
