import sys
from socket import *

def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py server_host server_port filename")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    clientSocket = socket(AF_INET, SOCK_STREAM)

    try:
        clientSocket.connect((server_host, server_port))
        request_line = f"GET /{filename} HTTP/1.1\r\n"
        header_line = f"Host: {server_host}\r\n\r\n"
        clientSocket.send(request_line.encode() + header_line.encode())

        response = b''
        while True:
            msg = clientSocket.recv(1024)
            if not msg:
                break
            response += msg

        print(response.decode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        clientSocket.close()




if __name__ == "__main__":
    main()