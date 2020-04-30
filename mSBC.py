#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""One line statement.

Author: Imran Matin

The client on the WaveGlider will be the mSBC. The reason for this is because
it will inly be run when it needs to issue commands to the cSBCs. As a client it will connect
to the cSBCs when it needs to issue a command to turn on (STANDBY), turn off (SHUTOFF), or
capture images (EVENT).
"""

import socket
import logging
from mSBC_config import *


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

    while True:
        try:
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
                # stats = s.recv(4096).decode("utf-8")
                # logger.info(f"Recieved: {stats}")

            # break forever loop if shutdown entered
            if command == COMMANDS[SHUTDOWN]:
                break
        except ConnectionRefusedError as e:
            # logger.error("Exception occurred", exc_info=True)
            logger.error(e)
        except:
            logger.error("Fatal Exception occurred", exc_info=True)
            break

    return 0


if __name__ == "__main__":
    """Create the logger and send messages to cSBC."""
    logger = createLogger()
    clientSend(logger)
