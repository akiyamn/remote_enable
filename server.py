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
    print(f"[{datetime.datetime.now()}] {message}")

def process_open():
    for process in psutil.process_iter():
        if PROCESS_NAME in process.name():
            return True
    return False

def start():
    program_open = process_open()
    if not program_open:
        subprocess.Popen(EXECUTABLE.split(" "))
        log(f"Executed {EXECUTABLE}.")
    else:
        log(f"Tried to run {EXECUTABLE} executable even though it was already open.")

def server_loop(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", port))
        log(f"Socket created on port {port}...")
        sock.listen(5)
        listening = True
        log("Server is now running.")
        while listening:
            connection, address = sock.accept()
            long_address = f"{address[0]}:{address[1]}"
            try:
                with connection:
                    connection.settimeout(TIMEOUT)
                    log(f"User at {long_address} connected.")
                    while connection:
                        data = connection.recv(1024)
                        clean_data = data.decode(errors="ignore").replace("\n", "").replace("\r", "")
                        log(f"{long_address} => {clean_data}")
                        response = interpret(clean_data, PROCESS_NAME, EXECUTABLE)
                        connection.sendall(response)
                        log(f"{long_address} <= {response.decode()}")
            except socket.timeout:
                log(f"{long_address} timed out.")
            except ConnectionAbortedError:
                log(f"{long_address} closed the connection.")
            except BrokenPipeError:
                log(f"{long_address} forcefully aborted the connection.")
            log(f"User at {address[0]}:{address[1]} disconnected.")

def interpret(command, process_name, executable):
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
    print(process.name() for process in psutil.process_iter())

if __name__ == "__main__":
    os.chdir(WORKING_DIR)
    server_loop(DEFAULT_PORT)
