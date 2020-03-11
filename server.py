import socket
import time
import threading
import sys


class Server:

    def __init__(self):
        self.port = self.getConfigFromFile()
        self.headerSize = 10
        self.serverSocket = self.setupServer()
        self.runServer()

    def getConfigFromFile(self):

        with open("serverProps.txt", "r") as serverFile:
            line = serverFile.readline()

        port = line.split("=", 1)[1]

        return int(port)

    def setupServer(self):
        # Socket to accept connections
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Bind host to a local host(for now) and to a specific port
        serverSocket.bind((self.get_ip(), self.port))

        serverSocket.listen(5)

        return serverSocket

    def client1To2(self, client1Socket, client2Socket):
        fullMsg = ""
        newMsg = True

        while True:
            msg = client1Socket.recv(32).decode("utf-8")
            fullMsg += msg

            if newMsg:
                msgLen = int(msg[:self.headerSize])
                newMsg = False

            if len(fullMsg) == self.headerSize + msgLen:
                print(f"Client1: {fullMsg[self.headerSize:]}")
                client2Socket.send(bytes(fullMsg, "utf-8"))
                fullMsg = ""
                newMsg = True

    def client2To1(self, client1Socket, client2Socket):
        fullMsg = ""
        newMsg = True

        while True:
            msg = client2Socket.recv(16).decode("utf-8")
            fullMsg += msg

            if newMsg:
                msgLen = int(msg[:self.headerSize])
                newMsg = False

            if len(fullMsg) == self.headerSize + msgLen:
                print(f"Client2: {fullMsg[self.headerSize:]}")
                client1Socket.send(bytes(fullMsg, "utf-8"))
                fullMsg = ""
                newMsg = True

    def get_ip(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            s.connect(('10.255.255.254', 1))
            ip = s.getsockname()[0]
        except socket.error:
            print("Private IP could not be found.")
            sys.exit()
        finally:
            s.close()

        return ip

    def runServer(self):

        print("Chatting with Friends Server \n\n")

        client1Socket, address1 = self.serverSocket.accept()
        print(f"Connection formed with {address1}")
        client2Socket, address2 = self.serverSocket.accept()
        print(f"Connection formed with: {address2}")

        t1 = threading.Thread(target=self.client1To2, args=[client1Socket, client2Socket])
        t2 = threading.Thread(target=self.client2To1, args=[client1Socket, client2Socket])

        t1.start()
        t2.start()

        t1.join()
        t2.join()


def main():

    myServer = Server()


main()
