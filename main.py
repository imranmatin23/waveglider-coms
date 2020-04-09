# Author: Imran Matin
# Description:
#   This file will initialize a camera and begin capturing images in a rolling buffer.
#   When it recieves the signal to save images, it stops capturing images and saves the current images in the rolling buffer.
#   Then it continues capturing images in a rolling buffer
#   When it recives the signal to shut down, it releases the camera and terminates the program


# Handles multiprocessing
from multiprocessing import Process, Value
# Import deque data structure to store rolling images
from collections import deque
# Import OpenCV
import cv2
# Import calls to handle camera
import EasyPySpin
# DEBUG
from time import sleep


# Maximum number of images in rolling buffer at once
ROLL_BUF_SIZE = 10


# DEBUG: Simulates input from mSBC
def testCameraStatus(cameraStatus, eventStatus):
    # DEBUG, test if camera stops
    print("Sleeping for 10 seconds...")
    sleep(10)

    print("Changing eventStatus to True...")
    eventStatus.value = True

    print("Sleeping for 10 seconds...")
    sleep(10)

    print("Changing eventStatus to True...")
    eventStatus.value = True
    
    print("Sleeping for 10 seconds...")
    sleep(10)

    print("Changing cameraStatus to False...")
    cameraStatus.value = False

    print("Sleeping for 10 seconds...")
    sleep(10)

    print("Exiting testCameraStatus()...")

# Simulates writing images from buffer to disk
# Currently does not actually write anything to disk
def writeImages(rollBuf):
    print("Writing images in rolling buffer to disk...")
    for i, img in enumerate(rollBuf):
        sleep(0.5)
        print("Wrote image {} to disk...".format(i))

    print("Completed writing images to disk...")

# Initalize camera and rolling buffer.
# Captures images in rolling buffer.
# Calls function to write rolling buffer images to disk when EVENT triggered. 
# Closes the camera when SHUTDOWN triggered.
def captureImages(cameraStatus, eventStatus): 
    # Create object to handle FLIR camera operations
    cap = EasyPySpin.VideoCapture(0)
    # Create rolling buffer for images
    rollBuf = deque(maxlen=ROLL_BUF_SIZE)

    while True:
        # DEBUG
        print("cameraStatus: {}".format(cameraStatus.value)) 
        print("eventStatus: {}".format(eventStatus.value)) 
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
            print("Finished writeImages()...")
        else:
            print("Recieved signal to terminate capturing images...")
            # release the camera and exit
            cap.release()
            print("Successflly released camera...")
            break

# Intializes shared variables for Processes
# Initalizes begins Processes for camera/rolling buffer and listening for commands
# Waits for camera/rolling buffer Process to terminate first
# Then waits for listening for commands Process to terminate
# Then terminates main function
if __name__ == "__main__":
    # shared variable across processes
    cameraStatus = Value('i', True)
    # shared variable for event statuses
    eventStatus = Value('i', False)

    # create a process with a target function
    p1 = Process(target=testCameraStatus, args=(cameraStatus, eventStatus, ))
    p2 = Process(target=captureImages, args=(cameraStatus, eventStatus, ))
    # start the process
    p1.start()
    p2.start()

    # check if processes are alive 
    print("Process p1 is alive: {}".format(p1.is_alive())) 
    print("Process p2 is alive: {}".format(p2.is_alive())) 

    # Stops execution of current program until this process completes.    
    p2.join()
    
    # check if processes are alive 
    print("Process p1 is alive: {}".format(p1.is_alive())) 
    print("Process p2 is alive: {}".format(p2.is_alive())) 

    # Stops execution of current program until this process completes.
    p1.join()

    # check if processes are alive 
    print("Process p1 is alive: {}".format(p1.is_alive())) 
    print("Process p2 is alive: {}".format(p2.is_alive())) 

    print("Execution of main is complete. Goodbye!")