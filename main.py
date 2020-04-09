# Author: Imran Matin
# Description:


## Main libraries
# Handles multiprocessing
from multiprocessing import Process, Value


## Camera libraries
# Import deque data structure to store rolling images
from collections import deque
# Import OpenCV
import cv2
# Import calls to handle camera
import EasyPySpin


## Server libraries
# Import socket module
import socket
# Import JSON module to load dict from string
import json
# Import sys to handle exceptions
import sys


## Camera constants
# Maximum number of images in rolling buffer at once
ROLL_BUF_SIZE = 10


## Server constants
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


# Simulates writing images from buffer to disk
# TODO: Currently does not actually write anything to disk
def writeImages(rollBuf):
    try: 
        print("Writing images in rolling buffer to disk...")
        for i, img in enumerate(rollBuf):
            # img.tofile('temp')
            print("Wrote image {} to disk...".format(i))

        print("Completed writing images to disk...")
    # capture all other exceptions
    except:
        e = sys.exc_info()[0]
        print("Error in writeImages: {}".format(e))

# Initalize camera and rolling buffer.
# Captures images in rolling buffer.
# Calls function to write rolling buffer images to disk when EVENT triggered. 
# Closes the camera when SHUTDOWN triggered.
def captureImages(cameraStatus, eventStatus, diskImages):
    try: 
        # Create object to handle FLIR camera operations
        cap = EasyPySpin.VideoCapture(0)
        # Create rolling buffer for images
        rollBuf = deque(maxlen=ROLL_BUF_SIZE)

        while True:
            if (cameraStatus.value and not eventStatus.value):
                # read frame, encode image, append to rolling buffer
                success, frame = cap.read()
                result, img = cv2.imencode('.png', frame)
                rollBuf.append(img)
                # DEBUG
                # print("Appending image: {}".format(img.size))
            elif (cameraStatus.value and eventStatus.value):
                # DEBUG
                print("Calling writeImages()...")
                writeImages(rollBuf)
                eventStatus.value = False
                diskImages.value += ROLL_BUF_SIZE
                print("Finished writeImages()...")
            else:
                print("Recieved signal to terminate capturing images...")
                # release the camera and exit
                cap.release()
                print("Successflly released camera...")
                break
    # capture all other exceptions
    except:
        e = sys.exc_info()[0]
        print("Error in captureImages: {}".format(e))
    finally:
        # release the camera and exit
        cap.release()
        print("Successflly released camera...")

# Handles client connections
def connectionHandler(cameraStatus, eventStatus, diskImages):
    # This is where the server begins continuously running until user interrupts with Keyboard
    try:
        # open a socket for this server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # bind to the port and wait for client connection
            s.bind((HOST, PORT))
            # 1 represents that we will queue 1 incoming connection before denying any other requests.
            s.listen(NUM_CONN)
            while True:
                # DEBUG
                print("Waiting for connection...")
                print("eventStatus is {}.".format(eventStatus.value))
                print("cameraStatus is {}.".format(cameraStatus.value))
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

                    if (data == STANDBY):
                        eventStatus.value = False
                        cameraStatus.value = True
                        conn.sendall(b'Keeping server in standby. Thank you for connecting.')
                    elif (data == EVENT):
                        eventStatus.value = True
                        cameraStatus.value = True
                        conn.sendall(b'Handled an event. Thank you for connecting.')
                    elif (data == SHUTDOWN):
                        eventStatus.value = False
                        cameraStatus.value = False
                        conn.sendall('Shutting off server. Captured {} images in total. Thank you for connecting.'.format(diskImages.value).encode('utf-8'))
                        break
    # capture all other exceptions
    except:
        e = sys.exc_info()[0]
        print("Error in connectionHandler: {}".format(e))

# Intializes shared variables for Processes
# Initalizes begins Processes for camera/rolling buffer and listening for commands
# Waits for camera/rolling buffer Process to terminate first
# Then waits for listening for commands Process to terminate
# Then terminates main function
if __name__ == "__main__":
    try:
        # shared variable across processes
        cameraStatus = Value('i', True)
        # shared variable for event statuses
        eventStatus = Value('i', False)
        # shared variable for number of images written to disk
        diskImages = Value('i', 0)

        # create a process with a target function
        p1 = Process(target=connectionHandler, args=(cameraStatus, eventStatus, diskImages, ))
        p2 = Process(target=captureImages, args=(cameraStatus, eventStatus, diskImages, ))
        # start the process
        p1.start()
        p2.start()

        # check if processes are alive 
        print("Process p1 is alive: {}".format(p1.is_alive())) 
        print("Process p2 is alive: {}".format(p2.is_alive())) 

        # Stops execution of current program until this process completes.    
        p2.join()
        p1.join()
        
        # check if processes are alive 
        print("Process p1 is alive: {}".format(p1.is_alive())) 
        print("Process p2 is alive: {}".format(p2.is_alive())) 

        print("Execution of main is complete. Goodbye!")
        # capture all other exceptions
    except:
        e = sys.exc_info()[0]
        print("Error in main: {}".format(e))