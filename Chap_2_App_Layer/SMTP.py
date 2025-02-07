from socket import *
import ssl
# Library for handling Secure Sockets Layer (SSL) and Transport Layer Security (TLS) protocols
# When we use the STARTTLS command, the program uses ssl to upgrade a regular TCP connection to an encrypted one
import base64
# For performing Base64 encoding and decoding
# During SMTP authentication, usernames and passwords need to be encoded in Base64 format
# $equired by the SMTP protocol since Base64 encoding ensures all authentication information can be safely
# transmitted as plain text without issues from special characters

username = "xxx@gmail.com"
pw = "aaaa bbbb cccc dddd"

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("smtp.gmail.com", 587)    #STARTTLS

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024).decode() # recv: string
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
ehloCommand = 'EHLO Alice\r\n'
# Necessary, because we are using STARTTLS and authentication, which require ESMTP (Extended SMTP) features
clientSocket.send(ehloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Start TLS
clientSocket.send("STARTTLS\r\n".encode())
rec0 = clientSocket.recv(1024).decode()
print(rec0)     # 220 2.0.0 Ready to start TLS

# Create SSL context and wrap socket
context = ssl.create_default_context()
'''
Creates a new SSL context with secure default settings
These defaults include:
    Modern SSL/TLS protocols
    Strong encryption ciphers
    Certificate verification settings
It's like preparing a secure "environment" for our connection
'''
secureSocket = context.wrap_socket(clientSocket, server_hostname=mailserver[0])
'''
Takes our existing regular socket (clientSocket)
Wraps it in SSL/TLS encryption using the context created above
Returns a new secure socket (secureSocket) that encrypts all communication
'''

# Authentication
auth_command = 'AUTH LOGIN\r\n'
secureSocket.send(auth_command.encode())
recv = secureSocket.recv(1024).decode()
print(recv)

secureSocket.send(base64.b64encode(username.encode()) + '\r\n'.encode())
recv = secureSocket.recv(1024).decode()
print(recv)

secureSocket.send(base64.b64encode(pw.encode()) + '\r\n'.encode())
recv = secureSocket.recv(1024).decode()
print(recv)

# Send MAIL FROM command and print server response.
mail_from_command = f"MAIL FROM: <{username}>\r\n"
secureSocket.send(mail_from_command.encode())
recv2 = secureSocket.recv(1024).decode()
print(recv2)

# Send RCPT TO command and print server response.
rcpt_to_command = "RCPT TO: <jj.huang.htp@gmail.com>\r\n"
secureSocket.send(rcpt_to_command.encode())
recv3 = secureSocket.recv(1024).decode()
print(recv3)

# Send DATA command and print server response.
data_command = "DATA\r\n"
secureSocket.send(data_command.encode())
recv4 = secureSocket.recv(1024).decode()
print(recv4)

# Send message data.
message_data = "hihi how are you?\r\nI'm JJ and you?\r\nTest for ehlo command\r\n"
secureSocket.send(message_data.encode())
# no response here because of no period

# Message ends with a single period.
period = ".\r\n"
secureSocket.send(period.encode())
recv6 = secureSocket.recv(1024).decode()
print(recv6)

# Send QUIT command and get server response.
ququ = "QUIT\r\n"
secureSocket.send(ququ.encode())
recv7 = secureSocket.recv(1024).decode()
print(recv7)

secureSocket.close()
clientSocket.close()