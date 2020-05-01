# Author: Imran Matin
# Description: Use this to test what happens when cSBC is processing an event and then another event is triggered.

# Import socket module
import socket
from time import sleep

# The server's hostname or IP address
HOST = "127.0.0.1"
# The port used by the server
PORT = 65431

### BEGIN TEST


# wait period to allow for cSBC to place collect images
sleep(3)

# Send 5 back to back event requests
for i in range(0, 5):
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

# wait for cSBC to complete writing of previous event
sleep(5)

# Send 5 back to back event requests
for i in range(0, 5):
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

# wait for cSBC to complete writing of previous event
sleep(5)

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

print("Completed Test...")
