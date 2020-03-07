import socket
import time
import threading


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:

        s.connect(('10.255.255.254', 1))
        ip = s.getsockname()[0]

    except:
        ip = '127.0.0.1'
    finally:
        s.close()

    return ip


class Server:

    def __init__(self, port):
        self.port = port
        self.headerSize = 10

    def setupServer(self):
        # Socket to accept connections
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Bind host to a local host(for now) and to a specific port
        serverSocket.bind((socket.gethostname(), self.port))
        #serverSocket.bind((get_ip(), self.port))

        #Queue only two clients
        #Experiment later with that value
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

    def runServer(self):
        serverSocket = self.setupServer()

        print("Server has started")

        client1Socket, address1 = serverSocket.accept()
        print(f"Connection formed with {address1}")
        client2Socket, address2 = serverSocket.accept()
        print(f"Connection formed with: {address2}")

        t1 = threading.Thread(target= self.client1To2, args=[client1Socket, client2Socket])
        t2 = threading.Thread(target= self.client2To1, args=[client1Socket, client2Socket])

        t1.start()
        t2.start()

        while True:
            print("Server is finished. Now sleeping.")
            time.sleep(600)


def main():

    myServer = Server(1234)
    myServer.setupServer()
    myServer.runServer()


main()
