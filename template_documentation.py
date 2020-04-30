#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""One line statement.

Author: Imran Matin

File is...
"""

import os
import time
import socket
import shutil
import logging
import datetime
import EasyPySpin
import multiprocessing as mp
from collections import deque
from cSBC_config import *


__author__ = "Imran Matin"
__copyright__ = "Copyright 2020, Innovative Marine Technology Lab, Scripps Institute of Oceanography"
__credits__ = ["Grant Deane, Dale Stokes"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Imran Matin"
__email__ = "imatin@ucsd.edu"
__status__ = "Development"


def createLogger():
    """Create logger for this SBC.

    It sets the basic configuration for the logger.

    ...

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
