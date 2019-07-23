#!/usr/bin/env python3

# Written by akiyamn on GitHub
# v1.0.0

import socket
import datetime

DEFAULT_PORT = 25564
TIMEOUT = 10

def connect(ip, port):
    # Establish a connection with a given ip and port number

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # A new TCP/IP socket
        sock.settimeout(TIMEOUT)  # Set a timeout if a connection can't be established
        sock.connect((ip, port))  # Attempt a connection
        address = f"{ip}:{port}"
        print(f"Connecting to {address}...")
        log(f"Connected to {address}.")
        help()  # Show help menu after connection

        command = ""
        while True:  # During a connection
            command = input("> ").lower()
            if command == "help":  # Show the help menu
                help()
            else:  # Send a command to the server
                try:
                    sock.sendall(command.encode(errors="ignore"))  # Send the command in binary to the server
                    data = sock.recv(1024)  # Attempt to receive data
                    response = data.decode(errors="ignore").replace("\n", "").replace("\r", "")  # Remove unwanted characters
                    process(response)  # Process the response from the server and return a corresponding message
                except BrokenPipeError:  # If the server suddenly disconnects
                    log(f"{address} timed you out or disconnected.")


def help():
    # Show a basic help/command screen

    print("\nCommands are:\nstatus : Checks the status of the server on the other end\nstart : Sends a message to start the application\nexit : Closes the connection\nhelp: Display this message\n")


def process(message):
    # Return the correct response to a message from a server

    responses = {
        "on": "Application is currently ON.",
        "off": "Application is currently OFF.",
        "done": "Application has been turned on.",
        "error": "An error occurred trying to run the application. It may already be running.",
        "what": "Server did not understand the previous request.",
    }

    if message != "":
        try:
            log(responses[message])
        except KeyError:
            log(f"Error: Unknown message received from server: \"{message}\".")


def log(message):
    # Adds the time and date to a print message

    print(f"[{datetime.datetime.now()}] {message}")


# Main block
if __name__ == "__main__":
    ip = input("Connect to: ")  # Ask for an IP
    port = input(f"Port (default is {DEFAULT_PORT}): ")  # Ask for a port
    port = DEFAULT_PORT if port == "" else int(port)  # Set port to default if one isn't provided
    connect(ip, port)  # Try to connect
