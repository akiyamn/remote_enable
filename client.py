import socket
import datetime

DEFAULT_PORT = 25564

def connect(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        address = f"{ip}:{port}"
        log(f"Connected to {address}.")

        command = ""
        while command != "exit":
            command = input("> ").lower()
            s.sendall(command.encode(errors="ignore"))
            data = s.recv(1024)
            response = data.decode(errors="ignore").split()[0]
            process(response)


def process(message):
    responses = {
        "on": "Server is currently ON.",
        "off": "Server is currently OFF.",
        "done": "Server has been turned on.",
        "error": "An error occurred trying to turn on the server. It may already be on.",
        "what": "Server did not understand the previous request.",
    }

    try:
        return responses[message]
    except KeyError:
        log(f"Error: Unknown message received from server: \"{message}\".")


def log(message):
    print(f"[{datetime.datetime.now()}] {message}")


if __name__ == "__main__":
    ip = input("Connect to: ")
    port = input(f"Port (default is {DEFAULT_PORT}): ")
    port = DEFAULT_PORT if port == "" else int(port)
    connect(ip, port)