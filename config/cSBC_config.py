"""Contains all the necessary configuration aspects for the cSBC module.

Author: Imran Matin
Email: imatin@ucsd.edu

Contains
- Camera Constants
- Server Constants
- Logging Constants
- Data Transfer Format
"""

########### Camera constants ###########
# Maximum number of images in rolling buffer at once
ROLL_BUF_SIZE = 150
# Location of image directory to save images
IMG_DIR = "images"
# Type of image to save to disk
IMG_TYPE = ".png"
# Amount of time in seconds to wait after event occurs
EVENT_DELAY = 5
# Camera Settings
EXPOSURE = 100000
GAIN = 10
BRIGHTNESS = 10
GAMMA = 0.25
FPS = 8
BACKLIGHT = 1


########### Server constants ###########
# The server's hostname or IP address
HOST = "0.0.0.0"
# The port used by the server
PORT = 65431
# number of connections that will be allowed to queue for this server
NUM_CONN = 0


########### Logging Constants ###########
# Name of file to log to
LOG_FILE = "logs/cSBC.log"
FILEMODE = "w"
LOGGER_NAME = "cSBC Logger"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
MESSAGE_FORMAT = "%(asctime)s.%(msecs)03d # %(name)s # %(levelname)s # %(message)s"


########### DATA TRANSFER FORMAT ###########
## Note: When adding new commands add the command to COMMANDS and a response in RESPONSES.
## Also add a case for the command in the `performCommands()` function and
## any other necessary locations that compute the necessary values.

# RESPONSES Responses to client
UPTIME_RESP = b"The server's uptime is %0.6f seconds."
EVENT_RESP = b"EVENT captured."
SHUTDOWN_RESP = b"Server SHUTDOWN. Captured %d images in total."


# COMMANDS
UPTIME = "UPTIME"
EVENT = "EVENT"
SHUTDOWN = "SHUTDOWN"
