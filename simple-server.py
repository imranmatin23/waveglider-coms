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
# Import subprocess to call code to take images
from subprocess import call
# Import deque data structure to store rolling images
from collections import deque
# Import OpenCV
import cv2
# Import calls to handle camera
import EasyPySpin
# Import sys to handle exceptions
import sys
# Handles multiprocessing
from multiprocessing import Process, Queue
# DEBUG
import time


# The server's hostname or IP address
HOST = '127.0.0.1'
# The port used by the server
PORT = 65432
# number of connections that will be allowed to queue for this server
NUM_CONN = 1
# Maximum number of images in rolling buffer at once
ROLL_BUF_SIZE = 10


# Captures images in rolling buffer
def captureImages(cap, roll_buf):
    try: 
        while True:
            # read a frame
            success, frame = cap.read()

            # encode and append to dequeue if image is not corrupt
            if success:
                result, img = cv2.imencode('.png', frame)
                if result:
                    roll_buf.append(img)
                    # DEBUG
                    print("Appending image: {}".format(img.size))
                else:
                    print("Error encoding image...")
    except:
        e = sys.exc_info()[0]
        print("Error when writing images: {}".format(e))
        return 1

# Saves images in rolling buffer
def writeImages(roll_buf):
    try:
        for img in roll_buf:
            img.tofile('temp')
        return 0  
    except:
        e = sys.exc_info()[0]
        print("Error when writing images: {}".format(e))
        return 1

# Handles client connections
def connectionHandler():
    # open a socket for this server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # bind to the port and wait for client connection
        s.bind((HOST, PORT))
        # 1 represents that we will queue 1 incoming connection before denying any other requests.
        s.listen(NUM_CONN)

        # This is where the server begins continuously running until user interrupts with Keyboard
        try:
            while True:
                # Establish connection with client. Waits here until client attempts to attach
                conn, addr = s.accept()

                # open the connection to the client
                with conn:
                    print('Got connection from', addr)
                    # recieve and decode command from client
                    # recv(BUFSIZE) is a blocking call, where BUFSIZE means read at most 1024 bytes"
                    # BUFSIZE should be a relatively small power of 2, for example 4096
                    data = conn.recv(1024).decode('utf-8')

                    # Do something with command
                    print("The data recieved from the client was: {}".format(data))

                    if (data == "SHUTOFF"):
                        break

                    if (data == "EVENT"):
                        result = 0
                        # return information back to client
                        if result == 0:
                            conn.sendall("Sucessfully captured images.\n".encode("utf-8"))
                        else:
                            conn.sendall("Encountered an issue when capturing images.\n".encode("utf-8"))

                    # close client connection
                    conn.sendall(b'Thank you for connecting.\n')

        # capture CTRL-C exception
        except KeyboardInterrupt:
            print("\nCaught keyboard interrupt, exiting.")
        # capture all other exceptions
        except:
            e = sys.exc_info()[0]
            print("Error: {}".format(e))
        # regardless of success or failure, release camera
        finally:
            cap.release()

# DEBUG:
def test():
    print("TESTING...")
    time.sleep(1)

if __name__ == '__main__':
    try:
        # Create object to handle FLIR camera operations
        cap = EasyPySpin.VideoCapture(0)
        # # Create rolling buffer for images
        # roll_buf = deque(maxlen=ROLL_BUF_SIZE)
        # # create multiprocessing queue to handle communication between processes
        # q = Queue()
        # create processes for the functions
        # p1 = Process(target=captureImages, args=(cap, roll_buf,))
        p1 = Process(target=test)
        p2 = Process(target=connectionHandler)

        # start the two process
        p1.start()
        p2.start()
        # print(q.get())    # prints "[42, None, 'hello']"
        # p.join()

    # capture CTRL-C exception
    except KeyboardInterrupt:
        print("\nCaught keyboard interrupt, exiting.")
    # capture all other exceptions
    except:
        e = sys.exc_info()[0]
        print("Error: {}".format(e))
    # regardless of success or failure, release camera
    finally:
        cap.release()



