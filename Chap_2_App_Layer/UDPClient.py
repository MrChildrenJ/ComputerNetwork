from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
# AF_INET: the underlying network is using IPv4
# SOCK_DGRAM: it is a UDP socket

while True:
    message = input('Input lowercase sentence: ')
    if message == "exit":
        exit(1)

    clientSocket.sendto(message.encode(), (serverName, serverPort))
    # message.encode(): convert message from string type to byte type

    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    # serverAddress includes IP and port
    # 2048: buffer size

    print(modifiedMessage.decode())

clientSocket.close()