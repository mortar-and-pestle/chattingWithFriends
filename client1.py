import socket

HEADER = 10

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((socket.gethostname(), 1236))

msg = "Hey client2!"
msg = f"{len(msg):<{HEADER}}" + msg

clientSocket.send(bytes(msg, "utf-8"))
print("Message sent!")

fullMsg = ""
newMsg = True

while True:
    msg = clientSocket.recv(16).decode("utf-8")

    if newMsg:
        msgLen = int(msg[:HEADER])
        newMsg = False

    fullMsg += msg

    if len(fullMsg) == HEADER + msgLen:
        print(fullMsg[HEADER:])
        break