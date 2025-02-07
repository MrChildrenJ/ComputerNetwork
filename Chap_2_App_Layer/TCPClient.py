from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)     # SOCK_STREAM: TCP
clientSocket.connect((serverName, serverPort))  # Before sending msg, need to establish connection first
# After this line, the 3-way handshake is performed and TCP connection is established

sentence = input('Input lowercase sentence: ')

clientSocket.send(sentence.encode())            # not sendto
modifiedMsg = clientSocket.recv(1024)           # not recvfrom
print('From Server ', modifiedMsg.decode())

clientSocket.close()