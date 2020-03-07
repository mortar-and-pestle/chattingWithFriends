import socket
import time


class Server:

    def __init__(self, port):
        self.port = port
        self.headerSize = 10

    def setupServer(self):
        # Socket to accept connections
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Bind host to a local host(for now) and to a specific port
        serverSocket.bind((socket.gethostname(), self.port))

        #Queue only two clients
        #Experiment later with that value
        serverSocket.listen(5)

        return serverSocket

    def runServer(self):
        serverSocket = self.setupServer()

        print("Server has started")

        while True:
            client1Socket, address1 = serverSocket.accept()
            print(f"Connection formed with {address1}")
            client2Socket, address2 = serverSocket.accept()
            print(f"Connection formed with: {address2}")

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
                    break

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
                    break

            while True:
                print("Server is finished. Now sleeping.")
                time.sleep(600)


def main():

    myServer = Server(1236)
    myServer.setupServer()
    myServer.runServer()


main()
