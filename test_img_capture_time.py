import sys
sys.path.append('../EasyPySpin/')
import cv2
import EasyPySpin
import time
from collections import deque

#
# Notes:
# imencode return (bool, numpy.ndarray) where it is (n, 1)
# the memory buffer in the documentation is just a regular array
# the numpy.ndarray has shape (n,m) where n is number fo rows and number of columns
# For 2D array, return a shape tuple with only 2 elements (i.e. (n,m))
# 

# Create object to handle FLIR camera operations
cap = EasyPySpin.VideoCapture(0)
# Create rolling buffer for images when in Standby Mode
roll_buf = deque(maxlen=10)
# DEBUG: Dummy variable acting as saving images signal
SAVE = 0
# DEBUG: Track deque
counter = 0

# Assume in STANDBY mode, where images are continuously being captured till signal given to save images

# DEBUG: Dummy time to turn SAVE signal to high
start_time = time.time()

# continuously capture images
while (True):

    if (counter > 60):
        break

    # DEBUG
    t = time.time() - start_time
    counter += 1
    if (t > 5):
        SAVE = 1
        start_time = time.time()

    # save the images
    if (SAVE):
        print()
        print("Saving images!")
        print()
        print(roll_buf[0][1].tofile('temp'))
        SAVE=0

    
    # read an image
    success, frame = cap.read()

    if success:
        # encode the image into an array
        result, img = cv2.imencode('.png', frame)

        # added to deque if valid image
        if result:
            roll_buf.append((counter, img))
        else:
            print("Error encoding image...")

    # print(roll_buf)
cap.release()
