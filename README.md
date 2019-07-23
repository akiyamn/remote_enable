# remote_enable
A basic server/client application written in Python (3.7) to remotely run executables on a server's system with feedback.

Some tinkering with the global variables is needed at the moment for `server.py` to point to your desired executable.

Each Python file only uses stock Python libraries, relying on its inbuilt
`socket` library for network communication.

## Requirements
### server.py
- a GNU/Linux machine (has not been tested anywhere else)
- Python 3
- psutil (via `pip install psutil`)
### client.py
- A GNU/Linux or Windows machine
- Python 3