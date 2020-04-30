## Server libraries
# Import socket module
import socket

# Import JSON module to load dict from string
import json

# Import sys to handle exceptions
import sys

# Import datetime to know current system time
from datetime import datetime as dt


from time import sleep

## Server constants
# The server's hostname or IP address
HOST = "127.0.0.1"
# The port used by the server
PORT = 65431
# number of connections that will be allowed to queue for this server
NUM_CONN = 0

EVENT = 0


def event():
    sleep_time = 3
    print(f"Sleeping for {sleep_time}")
    sleep(sleep_time)
    print("Stopped sleeping")
    EVENT = 0


if __name__ == "__main__":
    try:
        conns = []
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST, PORT))
                s.listen(NUM_CONN)
                # Establish connection with client. Waits here until client attempts to attach
                print(f"EVENT: {EVENT}")
                print("\nWaiting for connection...")
                conn, addr = s.accept()
                s.close()
                print(dt.now())
                # open the connection to the client
                with conn:
                    data = conn.recv(4096).decode("utf-8")

                    if data == "EVENT":
                        print("An EVENT occured...")
                        EVENT = 1
                        event()
                        print("The EVENT was completed...\n")
                    elif data == "SHUTDOWN":
                        print("Shutting Down...")
                        break
            print(dt.now())
    except Exception as e:
        print("\nException Occurred.")
        print(e)

    print("Exiting Main...")
