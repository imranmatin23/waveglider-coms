#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rapid Events Test.

Author: Imran Matin
Email: imatin@ucsd.edu

Usage:
# in a new terminal
python cSBC.py
# in a new terminal
python test_send_rapid_events.py

Tests the functionality of the cSBC when it is processing an event, and 
another event is triggered and sent to it. Functions as the mSBC. Note, change
the HOST variable to be the IP of the cSBC if you are not running it on the 
localhost. Set the number of events to be sent back to back and how many times
to send them.
"""

# Import socket module
import socket
from time import sleep

# The server's hostname or IP address
HOST = "127.0.0.1"
# The port used by the server
PORT = 65431
# Number of back to back events to be sent
NUM_EVENTS = 5
# Number of times to send NUM_EVENTS
NUM_TRIALS = 3


def send_events(num_events):
    """Sends num_events back to back commands to the cSBC."""
    # Send num_events back to back event requests
    for i in range(0, num_events):
        try:
            # open a socket for this client
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # connect to the server
                s.connect((HOST, PORT))
                print("Sending event")
                # send a command to the server
                s.sendall(b"EVENT")
                sleep(0.05)
        except Exception as e:
            print(f"\n{e}\n")


def send_shutdown():
    """Continuously sends shutdown command to cSBC until it is shutdown."""
    while True:
        try:
            # open a socket for this client
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # connect to the server
                s.connect((HOST, PORT))
                print("Sending shutdown")
                # send a command to the server
                s.sendall(b"SHUTDOWN")
                break
        except Exception as e:
            print(f"\n{e}\n")
            sleep(1)


if __name__ == "__main__":
    print("Starting Send Rapid Events Test...")
    try:
        for i in range(0, NUM_TRIALS):
            # wait period to allow for cSBC to place collect images
            sleep(5)
            send_events(NUM_EVENTS)

        # Shutdown the cSBC
        send_shutdown()
    except Exception as e:
        print(f"Exception Occurred")
        print("Completed Send Rapid Events Test...")
