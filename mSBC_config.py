# Author: Imran Matin
# Description: This file contains all the necessary configuration aspects for the mSBC module.

# The server's hostname or IP address
HOST = "127.0.0.1"
# The port used by the server
PORT = 65431


########### Logging Constants ###########
# Name of file to log to
LOG_FILE = "logs/mSBC.log"
FILEMODE = "w"
LOGGER_NAME = "mSBC Logger"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
MESSAGE_FORMAT = "%(asctime)s.%(msecs)03d # %(name)s # %(levelname)s # %(message)s"


# User strings
PROMPT = "What command would you like to send? [u,e,s]: "

#### DATA TRANSFER FORMAT DEFINED HERE ####
# define user choices
UPTIME = "u"
EVENT = "e"
SHUTDOWN = "s"
COMMANDS = {
    UPTIME: b"UPTIME",
    EVENT: b"EVENT",
    SHUTDOWN: b"SHUTDOWN",
}
