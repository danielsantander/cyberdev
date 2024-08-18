#!/usr/bin/env python3
#!/usr/bin/python3

"""
POLLEN8: Script that does some neat network stuff in Python.
"""

import argparse
import getpass
import ipaddress
import logging
import paramiko
import os
import socket
import struct
import sys
import threading
import time

from pathlib import Path
from typing import Tuple, Union
from utils import network, custom_logging

DEBUG_MODE = False
CWD = os.path.dirname(os.path.realpath(__file__))   # python/scripts/
SCRIPT_EPILOG = """\
Example:
    --ssh-server <ip_address> <port_number>
    --ssh-client <ip_address> <port_number>
    --ssh-cmd <ip_address> <username> <command> <port_number>
    --sniff
    --scan
"""

class Server(paramiko.ServerInterface):
    def __init__(self, _username:str='root', _passwd:str='fairbanks'):
        self.event = threading.Event()
        self._username = _username
        self._passwd = _passwd

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # credentials when connecting to server
        if (username == self._username) and (password == self._passwd):
            return paramiko.AUTH_SUCCESSFUL

class Host:
    def __init__(self, use_verbose:bool=DEBUG_MODE, **kwargs):
        self.hostname: str = socket.gethostname()
        self.ip_address: str = network.get_ip_address()
        log_lvl = logging.DEBUG if use_verbose else logging.INFO
        self._logger = custom_logging.create_console_logger(name="Host",level=log_lvl)

    def __str__(self) -> str:
        return f"{self.hostname} - {self.ip_address}"

class Pollen8:
    def __init__(self, use_verbose:bool=DEBUG_MODE, **kwargs):
        if use_verbose: self._logger.setLevel(logging.DEBUG)
        self.host : Host = Host(use_verbose=use_verbose)
        self.subnet : str = network.get_subnet(self.host.ip_address)
        log_lvl = logging.DEBUG if use_verbose else logging.INFO
        self._logger = custom_logging.create_console_logger(name="Pollen8", level=log_lvl)

    def __str__(self)->str:
        return f"{self.host.hostname} - {self.host.ip_address}"

    def check_port(self, ip_address:str, port:int, use_ipv4:bool=True, use_tcp:bool=True)->Tuple[bool,str]:
        """
        Opens socket to check port.
        Returns a tuple: True if port open, else False. Also returns the port banner if found.
        Example of Return data: (True, "Banner Message") | (True, None) | (False, None)
        """
        self._logger.info(f"scanning {ip_address}:{port}")
        status: bool = False
        banner: str = ""
        try:
            socket_family = socket.AF_INET if use_ipv4 else socket.AF_INET6       # IPV4 vs IPV6
            socket_type = socket.SOCK_STREAM if use_tcp else socket.SOCK_DGRAM    # TCP vs UDP
            s = socket.socket(socket_family, socket_type)
            s.settimeout(5) # Timeout in case of port not open
            s.connect((ip_address, port))
            # s.send(b"\x47\x45\x54\x20\x2f\x20\x48\x54\x54\x50\x2f\x31\x2e\x30\x2e\x2e\x2e\x2e")
            try:
                status = True
                banner = s.recv(1024).decode()
                self._logger.info(f"port {port} is open with banner {banner}")
            except:
                self._logger.info(f"port {port} is open")
            finally:
                s.close()
        except Exception as err:
            self._logger.info(f'port {port} is closed: {err}')
        finally:
            return status, banner

    def scan_target(self, ip_address:str, port_list:list=[]):
        max__port = 10000
        port_list = port_list if len(port_list) else [i for i in range(0,max__port)]
        self._logger.info(f"scanning {len(port_list)} ports on target {ip_address}")
        self._logger.debug(f"scanning ports: {port_list}")
        for port in port_list:
            t = threading.Thread(target=self.check_port, args=(ip_address, port))
            # t.start() # this breaks
            t.run()
        return

    def ssh_cmd(self, server:str, user:str, passwd:str, cmd:str, port:int=22)->list:
        """
        Make connection to ssh server and run single command.

        Keyword arguments:
        - ip: Server IP address
        - user: Server username
        - passwd: Username's password
        - cmd: command to run
        - port: port to connect to [defaults to 22]

        Returns list of output lines returned by the SSH server.
        """
        # TODO:
        #   - utilize using keys
        #   - modify to run multiple commands on SSH server
        #   - run commands on multiple SSH servers.
        client = paramiko.SSHClient()

        # bc we control both ends of connection, set policy to accept SSH key for the SSH server we're connecting to and make connection
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port=port, username=user, password=passwd)

        # assuming connection is made, run command and print each line of the output
        self._logger.info(f"starting SSH command: \"{cmd}\" ")
        _, stdout, stderr = client.exec_command(cmd)
        output = stdout.readlines() + stderr.readlines()
        if output:
            print('\n--- OUTPUT FROM SSH SERVER ---')
            for line in output:
                print(line.strip())
        return output

    def ssh_rcmd(self, server:str, port:str, user:str, passwd:str, command:str):
        import shlex
        import subprocess
        """
        Modification of ssh_cmd(). Run commands on Windows client over ssh.

        Keyword arguments:
        - server: Server IP address
        - port: Server port
        - user: username to connect to server
        - passwd: password to connect to server
        """
        ip = server if server is not None else input('Enter server IP: ')
        port = port if port is not None else input('Enter port: ')
        user = user if user is not None else getpass.getuser()
        passwd = passwd if passwd is not None else getpass.getpass()
        command = "exit" if command is None else command

        self._logger.info(f"ssh_rcmd: starting ssh client on {server}:{port} ...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=user, password=passwd)

        ssh_session = client.get_transport().open_session()
        if ssh_session.active:
            ssh_session.send(command)
            print(ssh_session.recv(1024).decode())  # read banner
            while(True):
                command = ssh_session.recv(1024)
                try:
                    cmd = command.decode()
                    if cmd == 'exit':
                        client.close()
                        break
                    cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                    ssh_session.send(cmd_output or 'okay')
                except Exception as e:
                    ssh_session.send(str(e))
            client.close()
        return

    def ssh_server(self, server:str=None, port:int=2222, rsa_key_file:Union[str,Path]=None):
        """
        Create SSH server for client to connect to.

        Keyword arguments:
        - server: Server IP address [defaults to host ip address]
        - port: Server port [defaults to 2222]
        - rsa_key_file: RSAKey [defaults to using `.ssh/id_sa` in home directory]
        """
        server = self.host.ip_address if server is None else server

        # RSA Key
        if not rsa_key_file:
            rsa_key_file = Path().home() / '.ssh' / 'id_rsa'
        else: rsa_key_file = rsa_key_file if isinstance(rsa_key_file, Path) else Path(rsa_key_file)
        assert(rsa_key_file.exists())
        rsa_key = paramiko.RSAKey(filename=rsa_key_file)

        try:
            self._logger.info(f'ssh_server: starting SSH server on {server}:{port}...')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((server, port))
            sock.listen(100)
            self._logger.info('[+] Listening for connection ...')
            client, addr = sock.accept()
        except Exception as e:
            self._logger.exception(f'[-] Listen failed: {e}')
            sys.exit(1)
        else:
            msg = f'[+] Got a connection! {client} {addr}'
            self._logger.info(msg)

        self._logger.debug('ssh_server: starting paramiko transport server for client connected')
        transport_session = paramiko.Transport(client)
        transport_session.add_server_key(rsa_key)
        server = Server()
        transport_session.start_server(server=server)

        chan = transport_session.accept(20)
        if chan is None:
            self._logger.warning('*** No channel, exiting...')
            sys.exit(1)

        self._logger.info('[+] Authenticated')
        self._logger.info(chan.recv(1024).decode())
        chan.send('Welcome to Pollen8 SHH server.')
        try:
            while True:
                command = input('Enter command: ').strip()
                if command != 'exit':
                    chan.send(command)
                    r = chan.recv(8192)
                    print(f'--- OUTPUT ---\n{r.decode()}\n')
                else:
                    self._logger.info('exiting ...')
                    chan.send('exit')
                    break
        except KeyboardInterrupt:
            transport_session.close()
            print ("\n")
        return

    def tcp_client(self, target_host:str, port:int=9998, timeout:int=5, message:bytes=b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")->str:
        """
        Make TCP connection to given target host and port, returns any message returned back.
        Keyword Arguments:
        - target_host (str): ip address of the host
        - port (int): port number [defaults to 9998]
        - timeout (int): timeout (seconds) [defaults to 5]
        - message (bytes): message to send [defaults to b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")]

        Returns: decoded response, or None if could not connect to target host.
        """
        self._logger.info(f"Sending TCP to: {target_host}:{port}")

        # create socket object
        #   AF_INET indicates use of standard IPv4 address or hostname
        #   SOCK_STREAM indicates TCP client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set timeout in case of port not open
        client.settimeout(timeout)

        try:
            # connect the client (TCP needs connection, unlike UDP)
            client.connect((target_host, port))

            # send some data (as bytes)
            self._logger.info(f"connected to target host, sending message: {message}")
            client.send(bytes(message))
        except Exception as err:
            self._logger.error(f'connection to target host failed: {err}')
            client.close()
            return None

        # receive some data
        response = client.recv(4096)
        resp_decoded = response.decode()
        client.close()
        self._logger.info(f"received message: {resp_decoded}")
        return resp_decoded

    def tcp_server(self, port:int=9998, timeout:int=5, response_message:bytes=b'ACKKK'):
        """
        Standard Multi-Threaded TCP Server

        Keyword Arguments:
        - port (int): port number [defaults to port 9998]
        - timeout (int): timeout (seconds) [defaults to 5]
        - response_message (bytes): response message to send back
        """
        host:str = '0.0.0.0'

        def handle_client(client_socket):
            with client_socket as sock:
                request = sock.recv(1024)
                self._logger.info(f'[*] Received: {request.decode("utf-8")}')
                sock.send(response_message)

        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((host, port))
            server.listen(timeout)
            self._logger.info(f'[*] Listening on {host}:{port}')
            while True:
                client, address = server.accept()
                self._logger.info(f'[*] Accepted connection from {address[0]}:{address[1]}')
                client_handler = threading.Thread(target=handle_client, args=(client,))
                client_handler.start()
        except KeyboardInterrupt:
            self._logger.info("KeyboardInterrupt: closing TCP server...")
            server.close()

    def udp_client(self, target_host:str, port:int=9998, timeout=5, message:bytes=b"AAABBBCCC"):
        """
        Send UDP message to the provided target and it's port.

        Keyword Arguments:
        - target_host (str): ip address of the host
        - port (int): port number [defaults to 9998]
        - timeout (int): timeout (seconds) [defaults to 5]
        - message (bytes): message to send [defaults to b"AAABBBCCC"]
        """
        self._logger.info(f"Sending UDP to {target_host}:{port} -- {message}")
        data = addr = None

        # create a socket object
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(timeout)

        # send some data - UDP is a connection-less protocol, there is no need to `connect()` first
        client.sendto(message, (target_host, port))

        try:
            # receive some data
            data, addr = client.recvfrom(4096)
            self._logger.info(f"data recv ({addr}): {data.decode()}")
        except socket.timeout as err:
            self._logger.info(f'UDP timed out ({timeout}s) with no response from server')

        client.close()
        return data, addr

    """
    def reverse_forward_tunnel(self, server_port, remote_host, remote_port, transport):
        transport.request_port_forward("", server_port)
        while True:
            # TODO: pull from rforward.py
            pass
    """

def main():
    def get_args():
        import textwrap
        parser = argparse.ArgumentParser(
            description="Pollen8 -- Script that does some neat network stuff.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(SCRIPT_EPILOG))
        list_of_choices = ['scan','sniff','ssh_client','ssh_server']
        parser.add_argument('action',
                choices=list_of_choices,
                action='store',
                type=str,
                help='Action to perform.')
        parser.add_argument('-v', '--verbose',
                            dest='verbose',
                            action='store_true',
                            default=DEBUG_MODE,
                            help=f'Debug mode. Defaults to {DEBUG_MODE}')
        parser.add_argument('-p','--port',
                            dest='port',
                            type=int,
                            action='store', help='Port value.')
        parser.add_argument('-i','--ip',
                            dest='ip_address',
                            type=str,
                            action='store', help='Host ip address.')
        args = parser.parse_args()
        return args

    def do_scan():
        """
        Scan subnet. Run: sudo python3 python/scripts/pollen8.py scan
        """
        from utils.network import Scanner, udp_sender
        scanner = Scanner()
        time.sleep(10)
        t = threading.Thread(target=udp_sender, args=(scanner.subnet,))
        t.start()
        scanner.sniff()

    def do_ssh_client():
        """
        Create SSH client to connect to SSH server. Run: python3 python/scripts/pollen8.py ssh_client --ip=192.168.0.100 --port 2222
        """

        cur_user = getpass.getuser()
        user = input(f'User [{cur_user}]: ') or cur_user
        passwd = getpass.getpass()
        # TODO: continue
        ip_address = args.ip_address or input(f'SSH Server IP Address to connect to: ')
        port = args.port or int(input("Port [2222]: ")) or 2222
        assert (ip_address and port)
        # command = input('Enter command: ')
        command = 'ClientConnected'
        diablo.ssh_rcmd(server=ip_address, port=port, user=user, passwd=passwd, command=command)
        return

    def do_ssh_server():
        ip_address = args.ip_address or diablo.host.ip_address
        server = ip_address or input('Enter server IP: ')
        port = args.port if args.port else input('Enter port [2222]: ') or 2222
        print(f"starting ssh server on: {server}:{port} ...")
        diablo.ssh_server(server=server, port=int(port)) # TODO: move ssh_server() method to network util library
        return

    ###########
    # MAIN
    ###########
    logging.getLogger("paramiko").setLevel(logging.DEBUG) # debug paramiko

    # args
    args = get_args()
    debug_mode = args.verbose is True or DEBUG_MODE
    diablo = Pollen8(use_verbose=debug_mode)

    # scan subnet
    if 'scan' == args.action: do_scan()

    # sniffer on local network
    elif 'sniff' == args.action: network.sniffer()

    # setup SSH server
    elif 'ssh_server' == args.action: do_ssh_server()

    # create SSH client
    elif 'ssh_client' == args.action: do_ssh_client()

    else: sys.exit()
    return

    ######################################################
    ######################################################

    if True: pass

    # Single command through SSH
    elif args.ssh_cmd is not None and len(args.ssh_cmd) >= 1:
        # expected ssh_cmd arg input: [ip, user, cmd, port]
        if str(args.ssh_cmd[0]).lower() == 'usage':
            print('\n\tUSAGE: ./pollen8 --ssh-cmd \{IP_ADDRESS\} {USERNAME} {COMMAND} {PORT}\n')
            sys.exit(1)

        user = args.ssh_cmd[1] if len(args.ssh_cmd) >=2 else input('User: ')
        passwd = getpass.getpass()
        cmd = args.ssh_cmd[2] if len(args.ssh_cmd) >= 3 else input('command: ')
        port = args.ssh_cmd[3] if len(args.ssh_cmd) >=4 else 22
        diablo.ssh_cmd(ip=args.ssh_cmd[0], port=int(port), user=user, passwd=passwd, cmd=cmd)

    else:
        print("no action, exiting . . .")
        sys.exit()

if __name__ == '__main__':
    main()