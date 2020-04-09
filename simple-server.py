# Laboratory: IMT, MPL Laboratory
# Researchers: Grant Deane and Dale Stokes
# Author: Imran Matin
# Description: The server on the WaveGlider will be the cSBCs. The reason for this is because
# they will be continuously waiting for a connection from the mSBC client. The client will connect
# and then send the command to turn on (STANDBY), turn off (SHUTOFF), or capture images (EVENT).
#
# Note: 1024 byte buffer size should be enough for the standard amount of data we will be transmitting.
# Hence there is no need to define our own message class if we can't. It would be good to have though.
#
# Note: Do not need to implement multiple connections for this server. The reason why is because only the
# mSBC will be connected to this server aka a cSBC and sending it commands.

# Import socket module
import socket
# Import JSON module to load dict from string
import json
# DEBUG
import sys

# The server's hostname or IP address
HOST = '127.0.0.1'
# The port used by the server
PORT = 65431
# number of connections that will be allowed to queue for this server
NUM_CONN = 1
# Define commands to be recieved from client
STANDBY = '{"eventStatus": 0, "cameraStatus": 1}'
EVENT = '{"eventStatus": 1, "cameraStatus": 1}'
SHUTDOWN = '{"eventStatus": 0, "cameraStatus": 0}'

# Handles client connections
def connectionHandler(eventStatus, cameraStatus):
    # open a socket for this server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # bind to the port and wait for client connection
        s.bind((HOST, PORT))
        # 1 represents that we will queue 1 incoming connection before denying any other requests.
        s.listen(NUM_CONN)

        # This is where the server begins continuously running until user interrupts with Keyboard
        try:
            while True:
                # DEBUG
                print("Waiting for connection...")
                print("eventStatus is {}.".format(eventStatus))
                print("cameraStatus is {}.".format(cameraStatus))
                print()

                # Establish connection with client. Waits here until client attempts to attach
                conn, addr = s.accept()

                # open the connection to the client
                with conn:
                    print('Got connection from', addr)
                    # recieve and decode command from client
                    # recv(BUFSIZE) is a blocking call, where BUFSIZE means read at most 1024 bytes"
                    # BUFSIZE should be a relatively small power of 2, for example 4096
                    data = conn.recv(1024).decode('utf-8')
                    print("The data recieved from the client was: {}".format(data))

                    # Do something with command
                    #   1) EVENT --> change eventStatus to True
                    #       - Return information about the images captured
                    #   2) SHUTOFF --> change cameraStatus to False
                    #       - Sent shutoff message
                    #       - close the server

                    # close client connection

                    if (data == STANDBY):
                        eventStatus = False
                        cameraStatus = True
                    elif (data == EVENT):
                        eventStatus = True
                        cameraStatus = True
                    elif (data == SHUTDOWN):
                        eventStatus = False
                        cameraStatus = False


                    conn.sendall(b'Thank you for connecting.\n')

        # capture CTRL-C exception
        except KeyboardInterrupt:
            print("\nCaught keyboard interrupt, exiting.")
        # capture all other exceptions
        except:
            e = sys.exc_info()[0]
            print("Error in connectionHandler: {}".format(e))


if __name__ == "__main__":

    global eventStatus
    global cameraStatus
    eventStatus = False
    cameraStatus = True

    print("Beginning main()...")
    print("Calling connectionHandler() to open server to connections...")
    connectionHandler(eventStatus, cameraStatus)
    print("Closed server to connections...")
    print("Exiting main()...")