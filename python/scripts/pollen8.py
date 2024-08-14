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

from typing import Tuple
from utils import network

DEBUG_MODE = False
CWD = os.path.dirname(os.path.realpath(__file__))
EPILOG = """\
Example:
    --ssh-server <ip_address> <port_number>
    --ssh-client <ip_address> <port_number>
    --ssh-cmd <ip_address> <username> <command> <port_number>
    --sniff
    --scan
"""

# debug paramiko
logging.getLogger("paramiko").setLevel(logging.DEBUG)

def get_args():
    import textwrap
    parser = argparse.ArgumentParser(
        description="Pollen8 -- Script that does some neat network stuff.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(EPILOG))
    parser.add_argument('-d', '--debug',
                        dest='debug',
                        action='store_true',
                        default=DEBUG_MODE,
                        help=f'Debug mode. Defaults to {DEBUG_MODE}')
    parser.add_argument('-p', '--port',
                        dest='port',
                        type=int,
                        action='store', help='Port value.')
    # nargs='+' takes 1 or more arguments, nargs='*' takes zero or more.
    parser.add_argument('--ssh-server',
                        dest='ssh_server',
                        metavar="IP PORT",
                        nargs="*",
                        action='store',
                        required=False,
                        help='Create SSH server. Input server ip address & port as arguments.')
    parser.add_argument('--ssh-client',
                        dest='ssh_client',
                        metavar="IP PORT",
                        nargs="*",
                        action='store',
                        required=False,
                        help='Create SSH client. Input server IP address as argument.')
    parser.add_argument('--ssh-cmd',
                        dest='ssh_cmd',
                        metavar="IP PORT",
                        nargs="+",
                        action='store',
                        required=False,
                        help='Make connection to SSH server and run single command')
    parser.add_argument('--sniff',
                        dest='sniff',
                        metavar="IP_ADDRESS/CIDR",
                        nargs="*",
                        action="store",
                        required=False,
                        help="Sniff network packet data.")
    parser.add_argument('--scan',
                        dest='scan',
                        action='store_true',
                        default=False,
                        help=f'Scan local network.')
    args = parser.parse_args()
    return args

def setup_logger(name:str=None, use_verbose:bool=False):
    """
    setup logger
    """
    lgr_lvl = logging.DEBUG if use_verbose else logging.INFO
    lgr_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    lgr_name = name if name is not None else str(__file__).split("/")[-1].split(".")[0].upper()
    logger = logging.getLogger(lgr_name)
    ch = logging.StreamHandler()
    ch.setLevel(lgr_lvl)
    ch.setFormatter(lgr_fmt)
    logger.addHandler(ch)
    # TODO: add RotatingFileHandler?
    logger.setLevel(lgr_lvl)
    return logger

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
    _logger = setup_logger("Host")
    def __init__(self, use_verbose:bool=DEBUG_MODE, **kwargs):
        self.hostname: str = None
        self.ip_address: str = None

        # init
        if use_verbose: self._logger.setLevel(logging.DEBUG)
        self.__get_hostname()
        self.__get_ip_address()

    def __get_hostname(self)->str:
        """ Get machine hostname via socket.gethostname() method. """
        if self.hostname is not None: return self.hostname
        self.hostname = socket.gethostname()
        return self.hostname

    def __get_ip_address(self)->str:
        """ Retrieve IP address (eth0 address) by creating UDP socket. """
        # src: https://stackoverflow.com/a/30990617/14745606
        if self.ip_address is not None: return self.ip_address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ip_address = s.getsockname()[0]
        return self.ip_address

    def __str__(self) -> str:
        return f"{self.hostname} - {self.ip_address}"\

class Pollen8:
    _logger = setup_logger("Pollen8")
    def __init__(self, use_verbose:bool=DEBUG_MODE, **kwargs):
        if use_verbose: self._logger.setLevel(logging.DEBUG)
        self.host:Host = Host(use_verbose=use_verbose)
        self.subnet:str = None

        self.__get_subnet()

    def __str__(self)->str:
        return f"{self.host.hostname} - {self.host.ip_address}"

    def __get_subnet(self, host_ip_address:str=None, subnet_mask:str="255.255.255.0", force:bool=False)->str:
        """
        Retrieve subnet for given host and mask.

        Keyword arguments:
        - host_ip_address (string): ip address of host
        - subnet_mask (string): defaults to 255.255.255.0

        src: https://stackoverflow.com/a/50867508/14745606
        """
        if self.subnet is not None and force is False: return self.subnet
        host_ip_address = self.host.ip_address if host_ip_address is None else host_ip_address
        iface = ipaddress.ip_interface(f"{host_ip_address}/{subnet_mask}")
        self.subnet = iface.network.__str__()
        return self.subnet

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

    def sniff(self, host_ip:str=None):#,subnet:str=None):
        """
        Sniffer for Windows and Linux machines.

        IMPORTANT: need to run using sudo

        Keyword Arguments:
        - host_ip (string): ip address/cidr
        # - subnet (string): subnet to sniff
        """

        # host_ip = socket.gethostbyname('localhost')   # 127.0.0.1
        host_ip = self.host.ip_address if host_ip is None else host_ip

        os_name = os.name
        self._logger.info(f"Starting sniffer on {host_ip} - {os_name} . . .")
        socket_protocol = socket.IPPROTO_IP if (os_name == 'nt') else socket.IPPROTO_ICMP
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host_ip, 0))

        # set sock option to include the IP header in the captured packets
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # enable promiscuous mode if on Windows by sending an IOCTL to the network card driver
        # (note may be issues running Windows on virtual machine, notification may be sent to user).
        if os_name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        # read one packet -- print out entire raw back w/o decoding
        # print(sniffer.recvfrom(65565))
        self._logger.info(f"raw packet (w/o decoding):\n{sniffer.recvfrom(65565)}")

        # continually read in and print out packets (read in the packet and  pass in the first 20 bytes)
        try:
            while True:
                # read packet
                raw_buffer = sniffer.recvfrom(65535)[0]

                # create IP header from the first 20 bytes
                ip_header = network.IP(raw_buffer[0:20])

                # if it's ICMP, we want it
                if ip_header.protocol == "ICMP":
                    # print the detected protocol and hosts:
                    print(f"Protocol: {ip_header.protocol} {ip_header.src_address} -> {ip_header.dst_address}")
                    print(f"Version: {ip_header.ver}")
                    print(f"Header Length: {ip_header.ihl} TTL: {ip_header.ttl}")

                    # calculate offset in raw packet where ICMP body starts
                    offset = ip_header.ihl * 4 # header length indicates number of 32-bit words (4 byte chunks) -- multiply by 4 to know the size of IP header, and next network layer ICMP begins
                    buf = raw_buffer[offset:offset+8]

                    # create ICMP struct
                    icmp_header = network.ICMP(buf)
                    print(f"ICMP -> Type: {icmp_header.type} Code: {icmp_header.code}\n")

        except KeyboardInterrupt:
            # Disable promiscuous mode if on Windows, before exiting script.
            if os_name == 'nt':
                sniffer.ioctl(socket.SID_RCVALL, socket.RCVALL_OFF)
            sys.exit()

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

    def ssh_server(self, server:str=None, port:int=2222, host_key:paramiko.RSAKey=None):
        """
        Create SSH server for client to connect to.

        Keyword arguments:
        - server: Server IP address [defaults to host ip address]
        - port: Server port [defaults to 2222]
        - host_key: paramiko.RSAKey [defaults to using `.ssh/id_sa` in home directory]
        """
        server = self.host.ip_address if server is None else server
        if host_key is None:
            # TODO: use home directory instead of CWD
            host_key = paramiko.RSAKey(filename=os.path.join(CWD, '.ssh/id_rsa'))
        self._logger.info(f'ssh_server: starting SSH server on {server}:{port}...')
        try:
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
        transport_session.add_server_key(host_key)
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
                command = input('Enter command: ')
                if command != 'exit':
                    chan.send(command)
                    r = chan.recv(8192)
                    # self._logger.info(r.decode())
                    print(f'--- OUTPUT ---\n{r.decode()}\n')
                else:
                    self._logger.info('exiting')
                    chan.send('exit')
                    break
        except KeyboardInterrupt:
            transport_session.close()
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
    global DEBUG_MODE

    args = get_args()
    DEBUG_MODE = args.debug is True or DEBUG_MODE
    diablo = Pollen8()

    # setup SSH server
    if args.ssh_server is not None:
        assert (isinstance(args.ssh_server, list))
        if len(args.ssh_server) == 0:
            server = input('Enter server IP: ')
            assert(server)
            port = input('Enter port [2222]: ') or 2222
        else:
            server , port = (args.ssh_server[0], int(args.ssh_server[1])) if len(args.ssh_server) == 2 else (args.ssh_server[0], 2222)
        diablo.ssh_server(server=server, port=int(port))

    # setup SSH client
    elif args.ssh_client is not None:
        cur_user = getpass.getuser()
        in_user = input(f'User [{cur_user}]: ')
        user = in_user or cur_user
        passwd = getpass.getpass()
        if len(args.ssh_client) == 0:
            server = input('Enter server IP: ')
            assert(server)
            port = input('Enter port [2222]: ') or 2222
        else:
            server , port = (args.ssh_client[0], args.ssh_client[1]) if len(args.ssh_client) == 2 else (args.ssh_client[0], '2222')

        # command = input('Enter command: ')
        command = 'ClientConnected'

        diablo.ssh_rcmd(server=server, port=port, user=user, passwd=passwd, command=command)

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

    # sniffer on local network
    elif args.sniff is not None:
        target:str = args.sniff[0] if len(args.sniff) >= 1 else (input("Enter IP address/CIDR: [127.0.0.0/8]: ") or '127.0.0.0/8')
        diablo.sniff(host_ip=target)

    # scan subnet
    elif args.scan is not None:
        from utils.network import Scanner, udp_sender
        scanner = Scanner()
        time.sleep(10)
        t = threading.Thread(target=udp_sender, args=(scanner.subnet,))
        t.start()
        scanner.sniff()


    else:
        print("no action, exiting . . .")
        sys.exit()

if __name__ == '__main__':
    main()