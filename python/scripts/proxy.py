#!/usr/bin/env python
#!/usr/bin/python3
"""
TCP Proxy
4 main parts:
- display the communication between the local and remote machines to the console (hexdump)
- receive data from an incoming socket from either the local or remote machine (receive_from)
- manage the traffic direction between remote and local machines (proxy_handler)
- set up a listener socket and pass it to our proxy_handler (server_loop)
"""

import sys
import socket
import threading
from typing import Union

DEBUG_MODE = False

# HEXFILTER string containing ASCII printable characters (if one exists) or a dot if representation does not exist.
#   - the representation of the printable character has a length of 3
#   - breakdown:
#       - For each integer in range 0-256, if the length of the corresponding character equals 3,
#         we get the character (chr(i)), otherwise we get a dot ('.').
#         Then join that list into a string to look like:
#         ................................ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[.]^_`abcdefghijklmnopqrstuvwxyz{|}~..................................¡¢£¤¥¦§¨©ª«¬.®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def hexdump(src:Union[str, bytes], length:int=16, show:bool=True):
    """
    Display the communication between the local and remote machines to the console.

    EXAMPLE:
        hexdump('python rocks\n and proxies roll\n')
    OUTPUT:
        0000  70 79 74 68 6F 6E 20 72 6F 63 6B 73 0A 20 61 6E   python rocks. an
        0010  64 20 70 72 6F 78 69 65 73 20 72 6F 6C 6C 0A      d proxies roll.
    """

    # ensure src is string
    if isinstance(src, bytes):
        src = src.decode()
    results = list()
    for i in range(0, len(src), length):
        # grab a piece of the string to dump and put into `word` variable
        word = str(src[i:i+length])

        # use translate to substitute the string representation of each character for the corresponding character in the raw string (printable)
        printable = word.translate(HEX_FILTER)

        # substitute the hex representation of the integer value of every character in the raw string (hexa)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3

        # create a new array to hold
        # - the strings that contains the hex value of the index of the first byte in the word,
        # - the hex value of the word
        # - and its printable representation
        results.append(f'{i:04x}  {hexa:<{hexwidth}}  {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results

def receive_from(connection):
    """
    Function for the two ends of the proxy to receive data.
    """

    # buffer to accumulate response from socket
    buffer = b""

    # set a five-second time-out
    # (increase timeout if necessary, e.g. proxying traffic to other countries over lossy networks)
    connection.settimeout(5)

    try:
        # read response data until no more data or timed out
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass

    return buffer

def request_handler(buffer):
    # perform packet modifications
    #   - perform fuzzing tasks
    #   - test for authentication issues
    #   - etc.
    return buffer

def response_handler(buffer):
    # perform packet modifications
    #   - perform fuzzing tasks
    #   - test for authentication issues
    #   - etc.
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # connect to remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # make sure no need to initiate connection to remote side and request data before starting loop
    # some server daemons expect this (FTP servers typically send a banner first, for example)
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            # remote_buffer = response_handler(remote_buffer)
            # client_socket.send(remote_buffer)
            # print("[==>] Sent to local.")

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print ("[<==] Sending %d bytes to localhost." % len(remote_buffer))
        client_socket.send(remote_buffer)

    # setup loop -> continuously read from local client, process data, send to remote client, read from remote client, process data, send to local client...
    # ... until no longer detect data to send.
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>] Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to local host.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data, Closing connections...")
            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    # create socket, bind lock host, and listen.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print('problem on bind: %r' % e)

        print("[!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)

    # when fresh connection comes in, hand off to proxy_handler in a new thread
    while True:
        client_socket, addr = server.accept()

        # print out the local connection information
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    input_args = {
        "local_host": sys.argv[1],
        "local_port": int(sys.argv[2]),
        "remote_host": sys.argv[3],
        "remote_port": int(sys.argv[4]),
        "receive_first": True if sys.argv[5] and str(sys.argv[5]).lower() in ['t', 'true'] else False
    }

    if DEBUG_MODE:
        for k,v in input_args.items(): print(f"{k}: {v}")

    server_loop(**input_args)
    return

if __name__ == '__main__':
    # hexdump('python rocks\n and proxies roll\n')
    main()