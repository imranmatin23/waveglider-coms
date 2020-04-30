# Laboratory: IMT, MPL Laboratory
# Researchers: Grant Deane and Dale Stokes
# Author: Imran Matin
# Description: The client on the WaveGlider will be the mSBC. The reason for this is because
# it will inly be run when it needs to issue commands to the cSBCs. As a client it will connect
# to the cSBCs when it needs to issue a command to turn on (STANDBY), turn off (SHUTOFF), or
# capture images (EVENT).

# Import socket module
import socket
import logging

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


def createLogger():
    """Create logger for this SBC."""
    logging.basicConfig(
        filename=LOG_FILE, filemode=FILEMODE, format=MESSAGE_FORMAT, level=logging.DEBUG
    )
    return logging.getLogger(LOGGER_NAME)


def readInput(logger):
    """Read user input from command line."""
    try:
        userInput = input(PROMPT)
        valid = True

        if userInput == STANDBY:
            command = COMMANDS[STANDBY]
        elif userInput == EVENT:
            command = COMMANDS[EVENT]
        elif userInput == SHUTDOWN:
            command = COMMANDS[SHUTDOWN]
        else:
            valid = False
            command = userInput
    except:
        logger.error("Exception occurred", exc_info=True)
        valid = False
        command = "Exception occurred"

    return command, valid


def clientSend(logger):
    """Send command to cSBC and recieve return message."""
    try:
        while True:
            # get user input
            command, valid = readInput(logger)
            if not valid:
                logger.warning(f"User inputted invalid command: {command}.")
                print()
                return 1

            # open a socket for this client
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # connect to the server
                s.connect((HOST, PORT))
                logger.info(f"Connected to cSBC at HOST={HOST} and PORT={PORT}.")

                # send a command to the server
                s.sendall(command)
                logger.info(f"Sent {command} to cSBC.")

                # wait till recieve stats back from server
                stats = s.recv(4096).decode("utf-8")
                logger.info(f"Recieved: {stats}")

            # break forever loop if shutdown entered
            if command == COMMANDS[SHUTDOWN]:
                break
    except:
        logger.error("Exception occurred", exc_info=True)

    return 0


if __name__ == "__main__":
    """Create the logger and send messages to cSBC."""
    logger = createLogger()
    clientSend(logger)
