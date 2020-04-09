# waveglider-coms
This repository is used to implement the network programming needed for the WaveGlider system to acquire images.

## File Descriptions
- Use `test_img_capture_time.py` to test how long it takes images to be taken.
- Use `simple-client.py` and `simple-server.py` for functionality of server.
- Use `simple-camera.py` for functionality of camera/rolling buffer. 
- Use `main.py` for full functionality with input from `simple-client.py`. 

## Issues, Questions, and TODOs
- How do I run rolling buffer to contiuosly capture images at the same time as listening for incoming data from client?
    - Multiprocessing.

- How do I make sure the images are captured fast enough?
    - Need to test.

- What data does mSBC want returned?
    - Need to ask.

- Need to clean and comment code. Need to implement production code with full exception handling and error checking.
    - TODO