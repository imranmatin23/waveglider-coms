#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Set Frame Rate Test.

Author: Imran Matin
Email: imatin@ucsd.edu

Usage:
# in a new terminal
python test_set_frame_rate.py

Sets the frame rate to FPS using Spinnaker's provided file.
"""

import PySpin

# The frame rate to set the camera to
FPS = 8


def run_single_camera(cam):
    """
    This function acts as the body of the example; please see NodeMapInfo example
    for more in-depth comments on setting up cameras.

    :param cam: Camera to run example on.
    :type cam: CameraPtr
    :return: True if successful, False otherwise.
    :rtype: bool
    """

    try:
        result = True

        # Retrieve TL device nodemap and print(device information
        nodemap_tldevice = cam.GetTLDeviceNodeMap()

        # result &= print_device_info(nodemap_tldevice)

        # Initialize camera
        cam.Init()

        # Retrieve GenICam nodemap
        nodemap = cam.GetNodeMap()

        node_acquisition_framerate = PySpin.CFloatPtr(
            nodemap.GetNode("AcquisitionFrameRate")
        )

        current_frame_rate = node_acquisition_framerate.GetValue()

        print("The current frame rate is %f..." % current_frame_rate)

        # if not PySpin.IsAvailable(node_acquisition_framerate) and not PySpin.IsReadable(
        #     node_acquisition_framerate
        # ):
        #     print("Unable to retrieve frame rate. Aborting...")
        #     return False

        # Range [1.0, 8.576685]
        node_acquisition_framerate.SetValue(FPS)

        framerate_to_set = node_acquisition_framerate.GetValue()

        print("Frame rate was set to %f..." % framerate_to_set)

        # Deinitialize camera
        cam.DeInit()

    except PySpin.SpinnakerException as ex:
        print("Error: %s" % ex)
        result = False

    return result


def main():
    """
    Example entry point; please see Enumeration example for more in-depth
    comments on preparing and cleaning up the system.

    :return: True if successful, False otherwise.
    :rtype: bool
    """

    # Retrieve singleton reference to system object
    system = PySpin.System.GetInstance()

    # Retrieve list of cameras from the system
    cam_list = system.GetCameras()

    num_cameras = cam_list.GetSize()

    print("Number of cameras detected:", num_cameras)
    # Finish if there are no cameras
    if num_cameras == 0:
        # Clear camera list before releasing system
        cam_list.Clear()

        # Release system
        system.ReleaseInstance()

        print("Not enough cameras!")
        input("Done! Press Enter to exit...")
        return False

    # Run example on each camera
    for i in range(num_cameras):
        cam = cam_list.GetByIndex(i)

        print("Running example for camera %d..." % i)

        result = run_single_camera(cam)
        print("Camera %d example complete..." % i)

    # Release reference to camera
    del cam

    # Clear camera list before releasing system
    cam_list.Clear()

    # Release instance
    system.ReleaseInstance()

    input("Done! Press Enter to exit...")
    return result


if __name__ == "__main__":
    main()
