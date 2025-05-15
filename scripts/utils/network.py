#!/usr/bin/env python
#!/usr/bin/python3

import argparse
import ipaddress
import logging
import os
import paramiko
import socket
import struct
import sys
import threading
import time
from pathlib import Path
from typing import Union, List, Tuple, Optional

DEBUG_MODE : bool = False
DEFAULT_USER : str = 'root'
DEFAULT_PASSWORD : str = 'fairbanks'

# HEX_FILTER string containing ASCII printable characters (if one exists) or a dot if representation does not exist.
#   - the representation of the printable character has a length of 3
#   - breakdown:
#       - For each integer in range 0-256, if the length of the corresponding character equals 3,
#         we get the character (chr(i)), otherwise we get a dot ('.').
#         Then join that list into a string to look like:
#         ................................ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[.]^_`abcdefghijklmnopqrstuvwxyz{|}~..................................¡¢£¤¥¦§¨©ª«¬.®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

def setup_logger(name:Optional[str]=None, use_verbose:bool=DEBUG_MODE):
    """
    Setup and return a console logger.
    """
    lgr_lvl = logging.DEBUG if use_verbose else logging.INFO
    lgr_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    lgr_name = name if name is not None else str(__file__).split("/")[-1].split(".")[0].upper()
    logger = logging.getLogger(lgr_name)
    ch = logging.StreamHandler()
    ch.setFormatter(lgr_fmt)
    logger.addHandler(ch)
    logger.setLevel(lgr_lvl)
    return logger

logger = setup_logger()

class IP:
    """
    IP class that can read a packet and parse the header into it's own separate fields (map the first 20 bytes of the received buffer into a friendly IP header).

    Keyword Arguments:
    - buff (string): packet data

    Example:
    mypacket = IP(buff)
    print (f'{mypacket.src_address} -> {mypacket.dst_address}')
    """
    def __init__(self, buff):
        # first char '<' specifies endianness of the data (order of bytes within binary number)
        # B -> 1-byte unsigned char
        # H -> 2-byte unsigned short
        # s -> a byte array requiring byte-width specifications (4s means 4-byte string)
        header = struct.unpack('<BBHHHBBH4s4s', buff)

        # With first byte of header data:
        # - assign version variable (self.ver) the high-order nybble by right-shifting the byte by four places (prepending four 9s to the front)
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
            err_msg = ("%s No protocol for %s" % (e, self.protocol_num))
            logger.error(err_msg)
            self.protocol = str(self.protocol_num)

    def __str__(self) -> str:
        return f"{self.src_address} -> {self.dst_address}"


# IP class using ctype Struct Model
from ctypes import Structure, c_ubyte, c_ushort, c_uint32
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
    def _new_ (self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

class ICMP:
    """
    Class to decode ICMP messages and parse the header into it's own separate fields.

    Keyword Arguments:
    - buff (string) - ICMP body of packet
    """
    def __init__(self, buff):
        header = struct.unpack('<BBHHH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

class Scanner:
    def __init__(self, host:Optional[str]=None, subnet:Optional[str]=None, verbose_mode:bool=False, **kwargs):
        self.logger = kwargs.get('logger') or setup_logger("Scanner", verbose_mode)
        self.host = get_ip_address() if host is None else host
        self.subnet = get_subnet(self.host) if subnet is None else subnet
        logger.info(f"running scanner on host {self.host} ({self.subnet})")

        socket_protocol = socket.IPPROTO_IP if (os.name=='nt') else socket.IPPROTO_ICMP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((self.host, 0))

        # set sock option to include the IP header in the captured packets
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        logger.debug('Hitting promiscuous mode.')
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self, message:str="ACK!"):
        """
        Network sniffer that keeps track of which hosts are up.
        Usually called after making UDP calls with same message -- with udp_sender().

        If the anticipated ICMP message is detected:
            - check the ICMP response is coming from within the target subnet
            - check the ICMP response contains the message
        """
        hosts_up = set([f'{str(self.host)} *'])
        try:
            while True:
                print('.',end='')
                raw_buffer = self.socket.recvfrom(65535)[0] # read packet
                self.logger.debug(f"received raw_buffer: {raw_buffer}")

                # create IP header from the first 20 bytes
                ip_header = IP(raw_buffer[0:20])
                self.logger.debug(f"ip_header (protocol -- {ip_header.protocol}):\t{ip_header}")
                if ip_header.protocol == "ICMP":
                    # debugging print statements:
                    # print the detected protocol and hosts:
                    # print(f"Protocol: {ip_header.protocol} {ip_header.src_address} -> {ip_header.dst_address}")
                    # print(f"Version: {ip_header.ver}")
                    # print(f"Header Length: {ip_header.ihl} TTL: {ip_header.ttl}")

                    # calculate offset in raw packet where ICMP body starts
                    # header length indicates number of 32-bit words (4 byte chunks) -- multiply by 4 to know the size of IP header, and next network layer ICMP begins
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    self.logger.debug(f"buf value: {buf}")

                    # create ICMP struct
                    icmp_header = ICMP(buf)
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(self.subnet):
                            if raw_buffer[len(raw_buffer) - len(message): ] == bytes(message, 'utf-8'):
                                hosts_up.add(str(ip_header.src_address))
                                print(f"Host Up: {str(ip_header.src_address)}")
        # handle CTRL-C
        except KeyboardInterrupt:
            # disable promiscuous mode if on Windows, before exiting script
            if  os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

            self.logger.info('\nUser interrupted.')
            if hosts_up:
                print(f'\n\nSummary: Hosts up on {self.subnet}')
            for host in sorted(hosts_up):
                print(f'{host}')
            print('')
            sys.exit()
        except Exception as e:
            self.logger.error(f"ERROR: {e.__str__()}")
        return

class Server(paramiko.ServerInterface):
    def __init__(self, _username:str=DEFAULT_USER, _passwd:str=DEFAULT_PASSWORD):
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

def ip2long(ip:str)->int:
    packed = socket.inet_aton(ip)
    lng = struct.unpack("!L", packed)[0]
    return lng

def long2ip(lng:int)->str:
    packed = struct.pack("!L", lng)
    ip = socket.inet_ntoa(packed)
    return ip

def get_ip_address()->str:
    """
    Creates UDP socket to retrieve IP (eth0) address.

    sources:
        - https://stackoverflow.com/a/30990617/14745606
        - https://pythontic.com/modules/socket/gethostname
    """
    ip_address = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_subnet(host:Optional[str]=None, subnet_mask:str="255.255.255.0"):
    """
    Retrieve subnet given host and a subnet mask. For example, given subnet of 255.255.255.0, return value is 192.178.2.0/24

    Keyword arguments:
    - host (string): ip address
    - subnet mask (string): defaults to 255.255.255.0

    src: https://stackoverflow.com/a/50867508/14745606
    """
    host = get_ip_address() if host is None else host
    iface = ipaddress.ip_interface(f"{host}/{subnet_mask}")
    return iface.network  # 192.178.2.0/24 (given 192.178.2.10 with subnet 255.255.255.0)

def hexdump(data:Union[str,bytes], length:int=16, show:bool=False)->List[str]:
    """
    Display the communication between the local and remote machines to the console.

    EXAMPLE:
        hexdump('python rocks\n and proxies roll\n')
    OUTPUT:
        0000  70 79 74 68 6F 6E 20 72 6F 63 6B 73 0A 20 61 6E   python rocks. an
        0010  64 20 70 72 6F 78 69 65 73 20 72 6F 6C 6C 0A      d proxies roll.
    """
    # ensure data is string
    if isinstance(data, bytes):
        data = data.decode()
    results = list()
    for i in range(0, len(data), length):
        # grab a piece of the string to dump and put into `word` variable
        word = str(data[i:i+length])

        # use translate to substitute the string representation of each character for the corresponding character in the raw string (printable)
        printable = word.translate(HEX_FILTER)

        # substitute the hex representation of the integer value of every character in the raw string (hexa)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3

        # create a new array to hold
        # - the strings that contains the hex value of the index of the first byte in the word,
        # - the hex value of the word
        # - and its printable representation
        results.append(f'{i:04x}  {hexa:<{hexwidth}} {printable}')
    for line in results:
        logger.debug(line)
        if show: print(line)
    return results

def mail_sniffer():
    """
    Uses scapy to sniff packets focused on mail related ports.
    """
    from scapy.all import TCP, IP
    bpf_common_mail_ports = "tcp port 110 or tcp port 25 or tcp port 143" # 110 (POP3), 143 (IMAP), 25 (SMTP)

    def packet_callback(packet):
        """
        Callback function to be called for every packet. Checks for valid payload and if it contains USER or PASS mail command.
        """
        if packet[TCP].payload:
            mypacket = str(packet[TCP].payload)
            if 'user' in mypacket.lower() or 'pass' in mypacket.lower():
                print(f"[*] Destination: {packet[IP].dst}")     # server sending the data to
                print(f"[*] {str(packet[TCP].payload)}")        # actual data bytes of the packet
    packet_sniffer(clb=packet_callback, bpf=bpf_common_mail_ports)

def packet_sniffer(clb=None, bpf:Optional[str]=None, count:Optional[int]=None):
    from scapy.all import sniff
    """
    Uses scapy to sniff packets.

    Keyword Arguments:
    clb (function): callback function to be called for every packet
    bpf (str): packet filter using BPF (Berkeley Packet Filter) syntax
    count (int): how many packets to sniff, defaults to 1
    """

    # some packet filters:
    bpf_common_mail_ports = "tcp port 110 or tcp port 25 or tcp port 143" # 110 (POP3), 143 (IMAP), 25 (SMTP)
    bpf_ftp = "tcp port 21"

    def packet_callback(packet):
        """
        Callback function to be called for every packet.
        """
        print(packet.show())

    # setup params for sniffing
    params = {}
    params["prn"] = packet_callback if clb is None else clb
    if count: params["count"] = count
    if bpf:
        params["filter"] = bpf
        params["store"] = 0     # ensure packets are not kept in memory. (Good to use when running sniffer for long-term, so will not be consuming as much RAM)
    sniff(**params)

def scan_port(ip_address:str, port:int, timeout:Optional[int]=None, send_packet:bool=False, **kwargs)->Tuple[str,bool,str]:
    """
    Makes socket connection to port.

    Returns tuple with three values: asset scanned, if port is open, banner if found.
    Example: ('10.0.0.10:22', True, 'SSH-2.0-OpenSSH_7.9p1 Raspbian-10+deb10u4\r\n')

    src: https://www.geeksforgeeks.org/python-simple-port-scanner-with-sockets/#
    src: https://www.geeksforgeeks.org/how-to-get-open-port-banner-in-python/
    """
    ip_address = socket.gethostbyname(socket.gethostname()) if ip_address is None else ip_address
    packet = b"\x47\x45\x54\x20\x2f\x20\x48\x54\x54\x50\x2f\x31\x2e\x30\x2e\x2e\x2e\x2e"
    results: Tuple[str,bool,str] = (f"{ip_address}:{port}", False, "")
    try:
        # create socket object with:
        #  - AF_INET     -> using standard IPv4 address or hostname
        #  - SOCK_STREAM -> TCP client
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if timeout is not None: s.settimeout(timeout)
        s.connect((ip_address, port))
        if send_packet: s.send(packet)

        # try getting banner
        try:
            banner = s.recv(1024).decode()
            # print (f"port {port} is open with banner ({len(banner)}): {banner}")
            s.close()
            results = (f"{ip_address}:{port}",True,banner)
            kwargs.get("results", []).append(results)   # for threading purposes
        except Exception as err:
            # print (f"port {port} is open.")
            s.close()
            results = (f"{ip_address}:{port}", True, "")
            kwargs.get("results", []).append(results)   # for threading purposes
    except:
        # print (f"port {port} is closed.")
        results = (f"{ip_address}:{port}", False, "")
        kwargs.get("results", []).append(results)   # for threading purposes
    return results

def scan_ports(ip_address:str, ports:List[int]=list(range(0, 100000)), timeout:int=None, send_packet:bool=False)->List[Tuple[str,bool,str]]:
    """
    Utilizes threading to scan multiple ports.
    """
    threads = [None] * len(ports)
    results: List[Tuple[str,bool,str]] = []
    for idx, i in enumerate(ports):
        logger.debug(f"scanning {ip_address}:{i}") # DEBUGGING PURPOSES
        threads[idx] = threading.Thread(target=scan_port, kwargs={"ip_address": ip_address,"port": i, "timeout": timeout, "results": results}) #args=[i])
        threads[idx].start()

    # wait for all thread to finish
    for i in range(len(threads)):
        threads[i].join()

    # results: [('192.168.0.100:22', True, 'SSH-2.0-OpenSSH_7.9p1 Raspbian-10+deb10u4\r\n'), ('192.168.0.100:80', True, '')]
    # print (f"results ({type(results)} -- {len(results)}):\n{results}\n\n")
    return results

def sniffer(ip_address:str=None):
    """
    Packet sniffing on Windows and Linux machines. Need to run with sudo.

    Keyword Arguments:
    ip_address (str): ip address of machine to sniff
    """
    ip_address = ip_address or get_ip_address()
    os_name = os.name
    logger.info(f"Starting packet sniffer on {ip_address} ({os_name})")
    socket_protocol = socket.IPPROTO_IP if os_name == 'nt' else socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((ip_address, 0))

    # set sock option to include the IP header in the captured packets
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # enable promiscuous mode if on Windows by sending IOCTL to the network card driver
    # (note: may be issues running on Windows on virtual machine, notification may be sent to user).
    if os_name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0]
            logger.debug(f"raw_buffer: {raw_buffer}")
            ip_header = IP(raw_buffer[0:20])
            packet_info = {"Protocol": ip_header.protocol,"Version":ip_header.ver,"Header Length":ip_header.ihl,"TTL":ip_header.ttl}
            if ip_header.protocol == 'ICMP':
                # calculate the offset in the raw packet where ICMP body lives
                offset = ip_header.ihl * 4
                buf = raw_buffer[offset:offset + 8]
                icmp_header = ICMP(buf)
                packet_info["ICMP"] = {"Type":icmp_header.type,"Code":icmp_header.code}
            logger.info(f"{ip_header}: {packet_info}")
    except KeyboardInterrupt:
        # if on Windows, turn off promiscuous mode
        if os_name == 'nt': sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        print("")
    return

def ssh_command(ip, port, user, passwd, cmd):
    """
    Make connection to ssh sever and run single command.

    Keyword arguments:
    - ip: server ip address
    - port: server port
    - user: username
    - passwd: user password
    - cmd: command to run
    """
    # TODO:
    #   - utilize using keys
    #   - modify to run multiple commands on SSH server
    #   - run commands on multiple SSH servers.
    #   - note: Paramiko also supports auth w/ keys instead of password auth

    client = paramiko.SSHClient()

    # bc we control both ends of connection,
    # set policy to accept SSH key for the SSH server we're connecting to and make connection
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    # assuming connection is made, run command and print each line of the output
    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('--- OUTPUT ---')
        for line in output:
            print(line.strip())
    else: print ('--- NO OUTPUT ---')
    return

def ssh_server(server:str=None, port:int=2222, rsa_key_file:Union[str,Path]=None, **kwargs):
        """
        Create SSH server for client to connect to.

        Keyword arguments:
        - server: Server IP address [defaults to host ip address]
        - port: Server port [defaults to 2222]
        - rsa_key_file: RSAKey [defaults to using `.ssh/id_sa` in home directory]
        """
        lgr = kwargs.get('logger', logger)
        server = server if server else get_ip_address()

        # RSA Key
        if not rsa_key_file:
            rsa_key_file = Path().home() / '.ssh' / 'id_rsa'
        else: rsa_key_file = rsa_key_file if isinstance(rsa_key_file, Path) else Path(rsa_key_file)
        assert(rsa_key_file.exists())
        rsa_key = paramiko.RSAKey(filename=rsa_key_file)

        try:
            lgr.info(f'starting SSH server on {server}:{port}...')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((server, port))
            sock.listen(100)
            lgr.info('[+] Listening for connection ...')
            client, addr = sock.accept()
        except Exception as e:
            lgr.error(f'[-] Listen failed, exiting. Error returned: {e.__str__()}')
            sys.exit(1)
        else:
            msg = f'[+] Got a connection! {client} {addr}'
            lgr.info(msg)

        lgr.debug('[+] Starting paramiko transport with connected client ...')
        transport_session = paramiko.Transport(client)
        transport_session.add_server_key(rsa_key)
        server = Server()
        transport_session.start_server(server=server)

        chan = transport_session.accept(20)
        if chan is None:
            lgr.warning('[-] No channel, exiting...')
            sys.exit(1)

        lgr.info(f'[+] Authenticated. Received message: \'{chan.recv(1024).decode()}\'')
        chan.send('Welcome to Pollen8 SHH server.')
        try:
            while True:
                command = input('Enter command: ').strip()
                if command != 'exit':
                    chan.send(command)
                    r = chan.recv(8192)
                    print(f'--- OUTPUT ---\n{r.decode()}\n')
                else:
                    lgr.info('[+] successfully quit, exiting ...')
                    transport_session.close()
                    break
        except KeyboardInterrupt:
            transport_session.close()
        print ("\n")
        return

def udp_sender(subnet:str, message:str="ACK!"):
    """
    Sends UDP datagrams to all IP address for given subnet and message.
    """
    # TODO: provide blacklist of addresses to skip?
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(subnet).hosts():
            time.sleep(1)
            print('+', end='')
            sender.sendto(bytes(message, 'utf8'), (str(ip), 65212))

if __name__ == '__main__':
    def get_args():
        list_of_choices = [
            'get_ip_address',
            # 'get_subnet',
            # 'udp_sender',
            'hexdump',
            'scanner',
            'scan_port', 'scan',
            'sniffer',
        ]
        # TODO: add ip_address and port args, use instead of --data
        parser = argparse.ArgumentParser()
        parser.add_argument('-d','--debug',
            dest='debug',
            action='store_true',
            default=False,
            help=f'Debug mode. [defaults to False]')

        # list of actions to use
        parser.add_argument('action',
            choices=list_of_choices,
            action='store',
            type=str,
            help='Action to perform.')
        parser.add_argument('--data',
            dest="data",
            action="store",
            type=str,
            help="Data to processes.")
        args = parser.parse_args()
        if args.action in ['hexdump'] and not args.data:
            parser.error(f'The \'{args.action}\' action requires data input.')
        return vars(args)

    # main
    args = get_args()

    action = args['action']
    data = args.get('data')
    debug = args.get('debug', DEBUG_MODE)
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("-"*50)
        logger.debug(f"args ({type(args)}): {args} ")
        logger.debug(f"action: {action}")
        logger.debug(f"data: {data}")
        logger.debug("-"*50 + "\n")

    results = None
    if action == 'get_ip_address':
        results = get_ip_address()
        print (f"{results}")

    elif action == 'hexdump':
        results = hexdump(data, show=True)

    elif action == 'scan_port' or action == 'scan':
        host_ip = get_ip_address()
        start_time = time.time()
        params = {"ip_address": host_ip}
        params['timeout'] = 5 # seconds

        # validate data
        if data:
            # python3 network.py scan_port --data 10.0.0.10
            import re
            import constants
            match = re.match(constants.RE_IP_ADDRESS, data)
            if match:
                params["ip_address"] = match.groupdict().get('ip_address', host_ip)
                params["ports"] = [int(match.groupdict().get('port'))] if match.groupdict().get('port') else list(range(0, 100000))
                # print(f"params: {params}")
                results = scan_ports(**params)
            else:
                params["ip_address"] = host_ip
                params["port"] = int(data)
                results = scan_port(**params)
        else:
            results = scan_ports(host_ip, ports=list(range(0,100000)))
        print("\n".join([f"{x[0]}\t{x[1]}\t{x[2]}" for x in results if x[1]]))
        end_time = time.time()
        logger.info(f"Time to finish scan (seconds) : {end_time-start_time}")

    elif action == 'sniffer':
        # sudo python3 ./network.py sniffer -d --data "10.0.0.10"
        ip_address = data or get_ip_address()
        sniffer(ip_address)

    elif action == 'scanner':
        # sudo python3 network.py scanner
        ip_address = data or get_ip_address()
        message : str = sys.argv[2] if len(sys.argv) >= 3 else 'ACK!'
        # print (f"using message: {message}")
        scanner = Scanner(ip_address, verbose_mode=debug)
        time.sleep(10)
        t = threading.Thread(target=udp_sender, args=[scanner.subnet,message])
        t.start()
        scanner.sniff(message=message)
    else:
        print("Unknown action.")
        sys.exit(1)
