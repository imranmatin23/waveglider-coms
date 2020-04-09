# Laboratory: IMT, MPL Laboratory
# Researchers: Grant Deane and Dale Stokes
# Author: Imran Matin
# Description: The client on the WaveGlider will be the mSBC. The reason for this is because
# it will inly be run when it needs to issue commands to the cSBCs. As a client it will connect
# to the cSBCs when it needs to issue a command to turn on (STANDBY), turn off (SHUTOFF), or 
# capture images (EVENT).

# Import socket module
import socket

# The server's hostname or IP address
HOST = '127.0.0.1'
# The port used by the server
PORT = 65432
# DEBUG
COMMAND = b"EVENT"

# open a socket for this client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # connect to the server
    s.connect((HOST, PORT))

    # send a command to the server
    s.sendall(COMMAND)

    # wait till recieve stats back from server
    # recv(BUFSIZE) is a blocking call, where BUFSIZE means read at most 1024 bytes"
    # BUFSIZE should be a relatively small power of 2, for example 4096
    stats = s.recv(1024).decode('utf-8')

# Print out recieved data
print('Received:', stats)