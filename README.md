# waveglider-coms
This repository is used to implement the network programming needed for the WaveGlider system to acquire images.

Use simple-client.py and simple-server.py for functionality. Use test_img_capture_time.py to test how long it takes images to be taken.

Issues:
How do I run rolling buffer to contiuosly capture images at the same time as listening for incoming data from client?
Multiprocessing

How do I make sure the images are captured fast enough?