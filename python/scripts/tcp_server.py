#!/usr/bin/env python
#!/usr/bin/python3

"""
Standard Multi-Threaded TCP Server
"""

import socket
import threading

MAX_BACKLOG_OF_CONNECTIONS = 5

IP = '0.0.0.0'
PORT = 9998

def main():
    # create server and start listening
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP,PORT))
    server.listen(MAX_BACKLOG_OF_CONNECTIONS)
    print(f'[*] Listening on {IP}:{PORT}')

    while True:
        # Wait for an incoming connection, receive client socket and remote connection details
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')

        # create thread pointing to handle_client function
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(client_socket:socket):
    """
    Performs recv() and sends message back to the client.
    """
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')

if __name__ == '__main__':
    main()