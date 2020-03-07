import threading
import socket


def connectToServer(destIP, port):

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #clientSocket.connect(("192.168.1.119", 1234))
    clientSocket.connect((socket.gethostname(), 1234))

    return clientSocket


def recv(mySocket, headerLen):

    fullMsg = ""
    newMsg = True

    while True:

        msg = mySocket.recv(16).decode("utf-8")
        fullMsg += msg

        if newMsg:
            msgLen = int(msg[:headerLen])
            newMsg = False

        if headerLen + msgLen == len(fullMsg):
            print(fullMsg[headerLen:])
            fullMsg = ""
            newMsg = True


def send(mySocket, headerLen):

    while True:

        msg = input()
        lenMsg = len(msg)

        msg = f"{lenMsg:<{headerLen}}{msg}"

        mySocket.send(bytes(msg, "utf-8"))


def main():

    headerLen = 10
    mySocket = connectToServer("localHost", 1234)

    recvT = threading.Thread(target=recv, args=[mySocket, headerLen])
    sendT = threading.Thread(target=send, args=[mySocket, headerLen])

    recvT.start()
    sendT.start()

    while True:
        time.sleep(600)


main()
