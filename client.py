import threading
import socket
import time


def connectToServer(destIP, port):

    print("Attempting connection...")
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((destIP, port))
    print("You are now connected to the server!\n")

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

    print("Chat away!\n")

    while True:

        msg = input()
        lenMsg = len(msg)

        msg = f"{lenMsg:<{headerLen}}{msg}"

        mySocket.send(bytes(msg, "utf-8"))


def getDestIPandPort():

    print("Welcome to Chatting with Friends!\n")
    ip = input("Enter the IP address of the Server: ")
    port = int(input("Enter the port number of the Server: "))

    return ip, port


def main():

    #Each message passed to the socket contains a header describing the length of the message
    #Since the string must be parsed by the server/clients, a predetermined number of characters are used to
    #represent the length of the message
    headerLen = 10

    #Get IP and Port of server
    ip, port = getDestIPandPort()

    #Setup connection to server by creating socket
    mySocket = connectToServer(ip, port)

    #Create two threads
    #One thread prints any messages received from the server
    #The other thread constantly asks for user input and sends it the server
    recvT = threading.Thread(target=recv, args=[mySocket, headerLen])
    sendT = threading.Thread(target=send, args=[mySocket, headerLen])

    recvT.start()
    sendT.start()

    recvT.join()
    sendT.join()


main()
