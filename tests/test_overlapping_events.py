# Author: Imran Matin
# Description: Use this to test what happens when cSBC is processing an event and then another event is triggered.


# Import socket module
import socket
from time import sleep

# The server's hostname or IP address
HOST = "127.0.0.1"
# The port used by the server
PORT = 65431

for i in range(0, 5):
    # open a socket for this client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # connect to the server
        s.connect((HOST, PORT))
        print("Sending event")
        # send a command to the server
        s.sendall(b"EVENT")
        sleep(0.1)

# open a socket for this client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # connect to the server
    s.connect((HOST, PORT))
    print("Sending shutdown")
    # send a command to the server
    s.sendall(b"SHUTDOWN")
