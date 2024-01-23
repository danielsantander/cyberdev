#!/usr/bin/env python
#!/usr/bin/python3

"""
Create SSH server for client to connect to.
"""

import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))

# TODO B4 RUNNING: enter correct path to RSA key
# currently assuming running within home directory and './ssh/' directory is available
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, '.ssh/id_rsa'))


class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # TODO B4 RUNNING: enter credentials of expected client to connect to
        if (username == 'JohnDoe') and (password == 'password123'):
            return paramiko.AUTH_SUCCESSFUL

if __name__ == '__main__':
    # TODO B4 RUNNING: update with server IP address
    server = ''
    server = server or input('Enter server IP: ')
    ssh_port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print ('[+] Listening for connection ...')
        client, addr = sock.accept()
    except Exception as e:
        print (f'[-] Listen failed: {e}')
        sys.exit(1)
    else:
        print('[+] Got a connection!', client, addr)

    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)

    chan = bhSession.accept(20)
    if chan is None:
        print('*** No channel.')
        sys.exit(1)

    print('[+] Authenticated')
    print(chan.recv(1024))
    chan.send('Welcome to bh_ssh')
    try:
        while True:
            command = input('Enter command: ')
            if command != 'exit':
                chan.send(command)
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send('exit')
                print('exiting')
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()
