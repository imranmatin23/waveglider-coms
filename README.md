# WaveGlider Communications System

This repository is used to implement the network programming needed for the 
WaveGlider system to acquire images. Currently the cSBC file is configured for 
BubbleCam, but can be easily modified for other cameras.


## Deployment

* Confirm the camera is connected to the USB 3.0 port on the SBC, and the manual
settings on the camera lense are correct.
* For development, the two files below can be executed on the same SBC in
different terminals. This is done by setting the `HOST` constant in the 
`./config/mSBC_config.py` file to `127.0.0.1`. 
* For production, follow the same
processes below except set the `HOST` constant in the 
`./config/mSBC_config.py` file to the cSBC's ip address.


### cSBC
1. Open a new terminal

2. Confirm you are in the `spinnaker_py37` conda environment.

3. Execute the following command to begin acquiring images and receiving 
connections.
    ```
    python cSBC.py
    ```


### mSBC
1. Open a new terminal

2. Confirm you are in the `spinnaker_py37` conda environment.

3. Execute the following command to begin sending commands to the cSBC.
    ```
    python mSBC.py
    ```


## How It Works
Explain how the current system works. How the cSBC and the mSBC interact,
send commands, are configured, exceptions, etc.


## Testing
All tests are contained within the `tests` directory. Please navigate into the
`tests` directory first before running any tests.
- To display a single image run `test_capture_single_image.py`.
- To display a video stream run `test_video.py`.

Explain what the different tests are. How to run the test bench.


## Logging
How to set the logging, what is logged.

This [link](https://docs.python.org/3/library/logging.html#logrecord-attributes) 
contains all of the attributes that can be logged in one call to log.


## Configuration
How to set the configuration for the cameras.

This [link](https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-set) 
contains all of the camera settings that can be set using OpenCV.


## Defining New Commands
Explain how to define new commands for the system.


## System Architecture
Explain how the system is set up at a high level.


## System Specifications
Explain the specifics for each SBC and camera.

This is a [link](https://www.flir.com/products/blackfly-usb3?model=BFLY-U3-23S6C-C) 
to the specific camera that I am working with. The camera is the FLIR Blackfly 
USB3 MODEL: BFLY-U3-23S6C-C: 2.3 MP, 41 FPS, SONY IMX249, COLOR


## Improvements to be Made
* Set up a way to allow the mSBC to change the camera configurations through
a command.
* Set up a way to modularize the cSBC and mSBC into classes.
* Create specific files to handle the different cameras (BubbleCam, WhiteCap, 
etc.)
* 
