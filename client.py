#!/usr/bin/env python3

# Written by akiyamn on GitHub
# v1.0.0

import socket
import datetime

DEFAULT_PORT = 25564

def connect(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        address = f"{ip}:{port}"
        log(f"Connected to {address}.")
        help()
        command = ""
        while True:
            command = input("> ").lower()
            if command == "help":
                help()
            else:
                try:
                    s.sendall(command.encode(errors="ignore"))
                    data = s.recv(1024)
                    response = data.decode(errors="ignore").replace("\n", "").replace("\r", "")
                    process(response)
                except BrokenPipeError:
                    log(f"{address} timed you out or disconnected.")

def help():
    print("\nCommands are:\nstatus : Checks the status of the server on the other end\nstart : Sends a message to start the application\nexit : Closes the connection\nhelp: Display this message\n")

def process(message):
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
    print(f"[{datetime.datetime.now()}] {message}")


if __name__ == "__main__":
    ip = input("Connect to: ")
    port = input(f"Port (default is {DEFAULT_PORT}): ")
    port = DEFAULT_PORT if port == "" else int(port)
    connect(ip, port)
