#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Handles the logic and communication for the mSBC in the WaveGlider system.

Author: Imran Matin
Email: imatin@ucsd.edu

The client on the WaveGlider will be the mSBC. The reason for this is because
it will only be run when it needs to issue commands to the cSBCs. As a client 
it will connect to the cSBCs when it needs to issue a command to turn on 
(STANDBY), turn off (SHUTOFF), or capture images (EVENT). The log file for this
system can be found in ./logs/mSBC.log.
"""

import time
import socket
import logging
import sys

# imports constants for this file
from config.mSBC_config import *


def createLogger():
    """Create and sets the basic configuration for the logger for this SBC.

    Parameters
    ----------
    None

    Returns
    -------
    logger
        Returns a logger with the specified name.

    Raises
    ------
    None
    
    """
    logging.basicConfig(
        filename=LOG_FILE,
        filemode=FILEMODE,
        format=MESSAGE_FORMAT,
        datefmt=DATE_FORMAT,
        level=logging.DEBUG,
    )
    logger = logging.getLogger(LOGGER_NAME)
    logger.debug(f"Logger created for {__file__}.")
    return logger


def readInput(logger):
    """Read user input from the command line and selects the correct command.

    Parameters
    ----------
    logger : logging
        The logger for the mSBC.

    Returns
    -------
    command
        Returns a command that is translated from the user input into a command the cSBC expects.
    valid
        Returns a bool that explains if the user inputted a valid command or not.
        
    Raises
    ------
    None
    
    """
    try:
        # reads user input
        userInput = input(PROMPT)
        valid = True

        # selects correct system command based off of user input
        if userInput == UPTIME:
            command = COMMANDS[UPTIME]
        elif userInput == EVENT:
            command = COMMANDS[EVENT]
        elif userInput == SHUTDOWN:
            command = COMMANDS[SHUTDOWN]
        # handles invalid input
        else:
            valid = False
            command = userInput
            logger.warning(f"User inputted invalid command: {command}.")

    except:
        logger.error("Exception occurred", exc_info=True)
        valid = False
        command = EXCEPTION
        print()

    return command, valid


def sendData(command, logger):
    """Takes in a user command, connects to the cSBC and sends the command.

    Parameters
    ----------
    command : str
        The command to send to the cSBC.
    logger : logging
        The logger for the mSBC.

    Returns
    -------
    NONE
        
    Raises
    ------
    ConnectionRefusedError
        Handles when the cSBC is not accepting new connections.
        
    """
    try:
        # allow for connection server to begin listening again
        time.sleep(0.1)

        # open a socket for this client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # connect to the server
            s.connect((HOST, PORT))
            logger.info(f"Connected to cSBC at HOST={HOST} and PORT={PORT}.")

            # send a command to the server
            s.sendall(command)
            logger.info(f"Sent {command} to cSBC.")

            # wait till receive stats back from server
            # cannot send another command until receive response
            # if this line is commented out, cSBC will still not accept new commands until processed previous command completely
            stats = s.recv(4096).decode("utf-8")
            logger.info(f"Received: {stats}")

    except ConnectionRefusedError as e:
        logger.error(e)
    except:
        logger.error("Fatal Exception occurred", exc_info=True)
        sys.exit()


def clientSend(logger):
    """Send command to cSBC and receive return message.
    
    This function will shut down mSBC if it sends the shutdown command.

    Parameters
    ----------
    logger : logging
        The logger for the mSBC.

    Returns
    -------
    None
        
    Raises
    ------
    None
    
    """
    while True:
        try:
            # get user input
            command, valid = readInput(logger)

            # validate input
            if not valid:
                if command == EXCEPTION:
                    return
                else:
                    continue

            # send data to server
            sendData(command, logger)

            # break forever loop if shutdown entered
            if command == COMMANDS[SHUTDOWN]:
                break

        except:
            logger.error("Fatal Exception occurred", exc_info=True)
            break


if __name__ == "__main__":
    """Create the logger and send messages to cSBC.

    Parameters
    ----------
    None

    Returns
    -------
    None
        
    Raises
    ------
    None
    
    """
    print("\n\n************Starting Interactive mSBC************\n\n")
    logger = createLogger()
    clientSend(logger)
    print("\n\n************Completed Interactive mSBC************\n\n")
