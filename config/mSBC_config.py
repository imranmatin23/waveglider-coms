"""Contains all the necessary configuration aspects for the mSBC module.

Author: Imran Matin
Email: imatin@ucsd.edu

Contains
- Server Constants
- Logging Constants
- Data Transfer Format
"""

########### Server constants ###########
# The server's hostname or IP address
HOST = "127.0.0.1"
# The port used by the server
PORT = 65431
# Internal error strings
EXCEPTION = "EXCEPTION"


########### Logging Constants ###########
# Name of file to log to
LOG_FILE = "logs/mSBC.log"
FILEMODE = "w"
LOGGER_NAME = "mSBC Logger"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
MESSAGE_FORMAT = "%(asctime)s.%(msecs)03d # %(name)s # %(levelname)s # %(message)s"

########### DATA TRANSFER FORMAT ###########
## Note: When adding new commands add the command to USER INPUTS and COMMANDS. Also update the console strings.
## Also add a case for the command in the `readInput()` function.

# USER INPUTS
UPTIME = "u"
EVENT = "e"
SHUTDOWN = "s"

# COMMANDS
COMMANDS = {
    UPTIME: b"UPTIME",
    EVENT: b"EVENT",
    SHUTDOWN: b"SHUTDOWN",
}

########### CONSOLE STRINGS ###########
PROMPT = "What command would you like to send? [u,e,s]: "
