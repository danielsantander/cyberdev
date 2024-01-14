#!/usr/bin/env python
#!/usr/bin/python3

"""
A simple network client and server to push files, or act as a listener to provides command line access.
A netcat replacement script.
Program may be invoked to:
    - upload a file
    - execute a command
    - start a command shell

Example:
- setup listener and provide a command shell:
    ./netcat.py -t {target_ip_address} -p 5555 -l -c
- open another terminal and run in client mode (until it receives the EOF marker):
    ./netcat.py -t 192.168.0.8 -p 5555
"""

import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading
import logging

# setup logger
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setFormatter(log_formatter)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

def execute(cmd):
    """
    Receives a command, runs it, then returns the output as a string.
    """
    cmd = cmd.strip()
    if not cmd:
        return

    # Run command on local OS and returns output from the command.
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()


class NetCat:
    def __init__(self, args, buffer=None) -> None:
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # TCP client
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        """
        Delegates execution to two methods (listen or send).
        """
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def handle(self, client_socket:socket):
        """
        Perform file uploads, execute commands, and create an interactive shell (while performing as a listener).
        """
        # if command should be executed,
        # send command to execute function
        # and send output back on the socket
        if self.args.execute:
            logger.info("in execute mode")
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        # if file should be uploaded,
        # set up loop to listen for content on the listening socket
        # and receive data until there's no more data coming in.
        elif self.args.upload:
            logger.info("in upload mode")
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                    logger.debug(f"\tfile_buffer length: {len(file_buffer)}")
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        # if a shell is to be created
        # set up loop, send prompt to the sender, wait for command string to come back,
        # then execute command and return the output to sender.
        elif self.args.command:
            logger.info("in command mode")
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b' #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    logger.exception(f"sever killed: {e}")
                    self.socket.close()
                    sys.exit()

    def listen(self):
        """
        Bind the target and port and start listening in a loop.
        """
        logger.info('listening...')
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    def send(self):
        """
        Connect to target and port.
        Send buffer to target first, if exists.
        Manually close the connection with CTRL-C.
        """
        logger.info('\tconnecting...')
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            logger.debug('\thas buffer, sending data...')
            self.socket.send(self.buffer)

        try:
            # retrieve data from the target
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            logger.exception('User terminated.')
            self.socket.close()
            sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network client server tool',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''Example:
                                      netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
                                      netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload file
                                      netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
                                      echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
                                      netcat.py -t 192.168.1.108 -p 5555 # connect to server
                                     '''))
    parser.add_argument('-c', '--command', action='store_true', help='initialize command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()

    # if listener, invoke with empty buffer string
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode('utf-8'))
    nc.run()
