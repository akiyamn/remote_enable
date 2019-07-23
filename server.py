#!/usr/bin/env python3

# Written by akiyamn on GitHub
# v1.0.0

import psutil
import subprocess
import datetime
import os
import socket

WORKING_DIR = "/home/yui/Desktop/minecraft-july-2019/MCServer2019"
PROCESS_NAME = "test.sh"
EXECUTABLE = "konsole -e ./test.sh"
TIMEOUT = 120
DEFAULT_PORT = 25564


def log(message):
    # Adds the time and date to a print message

    print(f"[{datetime.datetime.now()}] {message}")


def process_open():
    # Returns if a given process is open on the machine (bool)

    for process in psutil.process_iter():
        if PROCESS_NAME in process.name():
            return True
    return False


def start():
    # Runs the executable contained in the global variables

    program_open = process_open()
    if not program_open:
        subprocess.Popen(EXECUTABLE.split(" "))
        log(f"Executed {EXECUTABLE}.")
    else:
        log(f"Tried to run {EXECUTABLE} executable even though it was already open.")


def server_loop(port):
    # The main server loop. Accepts connections and relays messages

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # Start a new TCP/IP socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow sockets to overlap (in case it doesn't close on exit)
        sock.bind(("", port)) # Bind the socket to the port specified
        log(f"Socket created on port {port}...")
        sock.listen(5) # Wait for a connection
        log("Server is now running.")

        while True:  # Keep accepting connections forever
            connection, address = sock.accept()  # Accept a connection
            long_address = f"{address[0]}:{address[1]}"
            try:
                with connection:
                    connection.settimeout(TIMEOUT) # Set a timeout for this connection
                    log(f"User at {long_address} connected.")

                    while connection:  # During a connection
                        data = connection.recv(1024) # Receive data from client
                        clean_data = data.decode(errors="ignore").replace("\n", "").replace("\r", "") # Remove unwanted characters
                        log(f"{long_address} => {clean_data}")
                        response = interpret(clean_data, PROCESS_NAME, EXECUTABLE)  # Come up with a response to the data receieved
                        connection.sendall(response)  # Send the response to the client
                        log(f"{long_address} <= {response.decode()}")

            except socket.timeout:  # If the client times out
                log(f"{long_address} timed out.")
            except ConnectionAbortedError:  # If the client send a message to close the connection
                log(f"{long_address} closed the connection.")
            except BrokenPipeError:  # If the client suddenly disconnects
                log(f"{long_address} forcefully aborted the connection.")

            log(f"User at {address[0]}:{address[1]} disconnected.")


def interpret(command, process_name, executable):
    # Interprets feedback from a client in order to respond
    # Returns a response code in binary to be sent to the client

    if command == "status":
        if process_open():
            return b"on"
        else:
            return b"off"
    elif command == "start":
        if process_open():
            return b"error"
        else:
            start()
            return b"done"
    elif command == "exit":
        raise ConnectionAbortedError
    else:
        return b"what"


def display():
    # DEBUG
    # Displays all processes open, used for debug purposes

    print(process.name() for process in psutil.process_iter())

# Main block
if __name__ == "__main__":
    os.chdir(WORKING_DIR)
    server_loop(DEFAULT_PORT)
