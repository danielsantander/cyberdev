#!/usr/bin/env python
#!/usr/bin/python3

"""
========
POLLEN8
========

Script that does some neat network stuff in Python.
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

from ctypes import *

DEBUG_MODE = False
CWD = os.path.dirname(os.path.realpath(__file__))
EPILOG = f"""\
Example:
    --ssh-server 192.168.0.100 2222
    --ssh-client 192.168.0.100
    --ssh-cmd 192.168.0.100 root "whoami" 22
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
                        help=f'Debug mode. [{DEBUG_MODE}]')
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
                        help='Create SSH server. Input server ip address & port as arguments.',
                    )
    parser.add_argument('--ssh-client',
                        dest='ssh_client',
                        metavar="IP PORT",
                        nargs="*",
                        action='store',
                        required=False,
                        help='Create SSH client. Input server IP address as argument.',
                    )
    parser.add_argument('--ssh-cmd',
                        dest='ssh_cmd',
                        metavar="IP PORT",
                        nargs="+",
                        action='store',
                        required=False,
                        help='Make connection to SSH server and run single command',
                    )
    parser.add_argument('--sniff',
                        dest='sniff',
                        metavar="IP_ADDRESS/CIDR",
                        nargs="*",
                        action="store",
                        required=False,
                        help="Sniff network packet data."
                        )
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

# ctype Struct Model
class IP_CTYPE(Structure):
    """
    IP class that can read a packet and parse the header into it's own separate fields.
    Class maps C data types to the IP header.
    """

    # ctypes.Structure requires a '_fields_' variable.
    # Fields defining parts of IP header,each field takes three args:
        # 1. name of field
        # 2. type of value it takes
        # 3. width in bits for the field
    _fields_ = [
        ("ihl",          c_ubyte,  4),    # 4 bit unsigned char
        ("version",      c_ubyte,  4),    # 4 bit unsigned char
        ("tos",          c_ubyte,  8),    # 1 byte char
        ("len",          c_ushort, 16),   # 2 byte unsigned short
        ("id",           c_ushort, 16),   # 2 byte unsigned short
        ("offset",       c_ushort, 16),   # 2 byte unsigned short
        ("ttl",          c_ubyte,  8),    # 1 byte char
        ("protocol_num", c_ubyte,  8),    # 1 byte char
        ("sum",          c_ushort, 16),   # 2 byte unsigned short
        ("src",          c_uint32, 32),   # 4 byte unsigned int
        ("dst",          c_uint32, 32)    # 4 byte unsigned int
    ]
    def _new_ (cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))


# Struct IP Model
class IP:
    """
    IP class that can read a packet and parse the header into it's own separate fields (map the first 20 bytes of the received buffer into a friendly IP header).

    Keyword Arguments:
    - buff (string): packet data

    Example:
    mypacket = IP(buff)
    print (f'{mypacket.src_address} -> {mypacket.dst_address}')
    """
    def __init__(self, buff=None):
        # first char '<' specifies endianness of the data (order of bytes within binary number)
        # B -> 1-byte unsigned char
        # H -> 2-byte unsigned short
        # s -> a byte array requiring byte-width specifications (4s means 4-byte string)
        header = struct.unpack('<BBHHHBBH4s4s', buff)

        # With first byte of header data:
        # - assign version variable the high-order nybble by right-shifting the byte by four places (prepending four 9s to the front)
        # - assign hdrlen variable (self.ihl) the lower-order nybble (last 4 bits of byte) by Using boolean AND with 0xF (00001111) - replacing first 4 bits with 0.
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF

        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        # human readable IP addresses
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        self.protocol_map = { 1: "ICMP", 6: "TCP", 17: "UDP" }

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            err_msg = ("%s No protocol f or %s" % (e,  self.protocol_num))
            print(err_msg)
            self.protocol = str(self.protocol_num)

    def __str__(self) -> str:
        return f"{self.src_address} -> {self.dst_address}"

class ICMP:
    """
    ICMP class that can decode a packet and parse the header into it's own separate fields.

    Keyword Arguments:
    - buff (string): packet data
    """
    def __init__(self, buff):
        # assign  1 byte to the first two attributes, and 2 bytes to the next three attributes
        header = struct.unpack('<BBHHH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

class Scanner:
    def __init__(self, host:str=None, use_verbose:bool=DEBUG_MODE):
        self._logger = setup_logger("scanner", use_verbose=use_verbose)
        self.host = self.get_ip_address() if host is None else host
        self.subnet = self.get_subnet(self.host)

        self._logger.debug(f"Initializing scanner on subnet {self.subnet} ...")

        socket_protocol = socket.IPPROTO_IP if (os.name=='nt') else socket.IPPROTO_ICMP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((self.host, 0))

        # set sock option to include the IP header in the captured packets
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        self._logger.debug('Hitting promiscuous mode.')
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    @classmethod
    def get_ip_address(self):
        """ Retrieve IP address (eth0 address) by creating UDP socket."""
        # src: https://stackoverflow.com/a/30990617/14745606
        # TODO: source to perhaps make socket into context manager
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    @classmethod
    def get_subnet(self, host:str, subnet_mask:str="255.255.255.0"):
        """
        Retrieve subnet given host and a subnet mask. For example, given subnet of 255.255.255.0, return value is 192.178.2.0/24

        Keyword arguments:
        - host (string): ip address
        - subnet mask (string): defaults to 255.255.255.0

        src: https://stackoverflow.com/a/50867508/14745606
        """
         # commented out for classmethod
        # host = self.host if host is None else host
        iface = ipaddress.ip_interface(f"{host}/{subnet_mask}")
        return iface.network  # 192.178.2.0/24 (given 192.178.2.10 with subnet 255.255.255.0)

    @classmethod
    def udp_sender(self, subnet, message:str="ACK!"):
        """
        Sends UDP datagrams to all IP address in given subnet.
        """
        # TODO: provide blacklist of addresses to skip?

         # commented out for classmethod
        # subnet = self.subnet if subnet is None else subnet
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
            for ip in ipaddress.ip_network(subnet).hosts():
                time.sleep(1)
                print('+', end='')
                sender.sendto(bytes(message, 'utf8'), (str(ip), 65212))

    def start(self, message:str="ACK!"):
        """
        Sniffer for Windows and Linux machines. Note: use sudo.

        Keyword Arguments:
        - message (string): simple string structure to test the response coming from UDP packets.
        """
        hosts_up = set([f'{str(self.host)} *'])
        try:
            while True:
                print('.',end='')
                # read packet
                raw_buffer = self.socket.recvfrom(65535)[0]

                self._logger.debug(f"received raw_buffer:\t{raw_buffer}") # debugging

                # create IP header from the first 20 bytes
                ip_header = IP(raw_buffer[0:20])
                self._logger.debug(f"ip_header (protocol -- {ip_header.protocol}):\t{ip_header}") # debugging

                if ip_header.protocol == "ICMP":
                    # print the detected protocol and hosts:
                    # print(f"Protocol: {ip_header.protocol} {ip_header.src_address} -> {ip_header.dst_address}")
                    # print(f"Version: {ip_header.ver}")
                    # print(f"Header Length: {ip_header.ihl} TTL: {ip_header.ttl}")

                    # calculate offset in raw packet where ICMP body starts
                    # header length indicates number of 32-bit words (4 byte chunks) -- multiply by 4 to know the size of IP header, and next network layer ICMP begins
                    offset = ip_header.ihl * 4
                    self._logger.debug(f"offset where ICMP body starts: {offset}")
                    buf = raw_buffer[offset:offset + 8]
                    self._logger.debug(f"buf val: {buf}")

                    # create ICMP struct
                    icmp_header = ICMP(buf)

                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(self.subnet):
                            if raw_buffer[len(raw_buffer) - len(message): ] == bytes(message, 'utf8'):
                                hosts_up.add(str(ip_header.src_address))
                                print(f'Host Up: {str(ip_header.src_address)}')

        # handle CTRL-C
        except KeyboardInterrupt:
            # Disable promiscuous mode if on Windows, before exiting script.
            if os.name == 'nt':
                self.socket.ioctl(socket.SID_RCVALL, socket.RCVALL_OFF)
            print('\nUser interrupted.')
            if hosts_up:
                print(f"\n\nSummary: Hosts up on {self.subnet}")
            for host in sorted(hosts_up):
                print(f"{host}")
            print('')
            sys.exit()

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

    """
    def reverse_forward_tunnel(self, server_port, remote_host, remote_port, transport):
        transport.request_port_forward("", server_port)
        while True:
            # TODO: pull from rforward.py
            pass
    """

    def sniff(self, host_ip:str=None, subnet:str=None):
        """
        Sniffer for Windows and Linux machines. Note: use sudo.

        Keyword Arguments:
        - host (string): ip address/cidr
        """

        # get host IP address of machine
        # hostname = socket.gethostname()

        # host_ip = socket.gethostbyname('localhost')   # 127.0.0.1
        host_ip = Scanner().get_ip_address() if host_ip is None else host_ip

        os_name = os.name
        self.logger.info(f"Starting sniffer on {host_ip} - {os_name} . . .")
        socket_protocol = socket.IPPROTO_IP if (os_name=='nt') else socket.IPPROTO_ICMP
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host_ip, 0))

        # set sock option to include the IP header in the captured packets
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # enable promiscuous mode if on Windows by sending an IOCTL to the network card driver (note may be issues running Windows on virtual machine, notification may be sent to user).
        if os_name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        # # read one packet -- print out entire raw back w/o decoding
        # print(sniffer.recvfrom(65565))

        # continually read in and print out packets (read in the packet and  pass in the first 20 bytes)
        try:
            while True:
                # read packet
                raw_buffer = sniffer.recvfrom(65535)[0]

                # create IP header from the first 20 bytes
                ip_header = IP(raw_buffer[0:20])

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
                    icmp_header = ICMP(buf)
                    print(f"ICMP -> Type: {icmp_header.type} Code: {icmp_header.code}\n")

        except KeyboardInterrupt:
            # Disable promiscuous mode if on Windows, before exiting script.
            if os_name == 'nt':
                sniffer.ioctl(socket.SID_RCVALL, socket.RCVALL_OFF)
            sys.exit()


    def ssh_cmd(self, ip, port, user, passwd, cmd):
        """
        Make connection to ssh server and run single command.

        Keyword arguments:
        - ip: Server IP address
        - port: Server port
        - user: Server username
        - passwd: Username's password
        - cmd: command to run
        """
        # TODO:
        #   - utilize using keys
        #   - modify to run multiple commands on SSH server
        #   - run commands on multiple SSH servers.
        client = paramiko.SSHClient()

        # bc we control both ends of connection, set policy to accept SSH key for the SSH server we're connecting to and make connection
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=user, password=passwd)

        # assuming connection is made, run command and print each line of the output
        self.logger.info(f'ssh_cmd: starting SSH command...')
        _, stdout, stderr = client.exec_command(cmd)
        output = stdout.readlines() + stderr.readlines()
        if output:
            print('--- OUTPUT ---')
            for line in output:
                print(line.strip())
        return

    def ssh_rcmd(self, server:str, port:str, user:str, passwd:str, command:str):
        import shlex
        import subprocess
        """
        Send commands from a SSH server to run on client.

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

        self.logger.info(f"ssh_rcmd: starting ssh client on {server}, {port}")
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

    def ssh_server(self, server:str, port:int=2222, host_key:paramiko.RSAKey=None):
        """
        Create SSH server for client to connect to.

        Keyword arguments:
        - server: Server IP address
        - port: Server port
        - host_key: paramiko.RSAKey
        """
        self.logger.info(f'ssh_server: starting SSH server on {server}, {port}...')
        if host_key is None:
            host_key = paramiko.RSAKey(filename=os.path.join(CWD, '.ssh/id_rsa'))
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((server, port))
            sock.listen(100)
            self.logger.info('[+] Listening for connection ...')
            client, addr = sock.accept()
        except Exception as e:
            self.logger.exception(f'[-] Listen failed: {e}')
            sys.exit(1)
        else:
            msg = f'[+] Got a connection! {client} {addr}'
            self.logger.info(msg)

        self.logger.debug('ssh_server: starting paramiko transport server for client connected')
        transport_session = paramiko.Transport(client)
        transport_session.add_server_key(host_key)
        server = Server()
        transport_session.start_server(server=server)

        chan = transport_session.accept(20)
        if chan is None:
            self.logger.warning('*** No channel, exiting...')
            sys.exit(1)

        self.logger.info('[+] Authenticated')
        self.logger.info(chan.recv(1024).decode())
        chan.send('Welcome to Pollen8 SHH server.')
        try:
            while True:
                command = input('Enter command: ')
                if command != 'exit':
                    chan.send(command)
                    r = chan.recv(8192)
                    # self.logger.info(r.decode())
                    print(f'--- OUTPUT ---\n{r.decode()}\n')
                else:
                    self.logger.info('exiting')
                    chan.send('exit')
                    break
        except KeyboardInterrupt:
            transport_session.close()
        return

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
        # input: [ip, user, cmd, port]
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
        # target:str = args.sniff[0] if len(args.sniff) >= 1 else (input("Enter IP address/CIDR: [127.0.0.0/8]: ") or '127.0.0.0/8')
        diablo.sniff()

    # scan local network
    elif args.scan is not None:
        scanner = Scanner()
        time.sleep(10)
        t = threading.Thread(target=scanner.udp_sender, args=(scanner.subnet,))
        t.start()
        scanner.start()


    else:
        print("no action, exiting . . .")
        sys.exit()

if __name__ == '__main__':
    main()