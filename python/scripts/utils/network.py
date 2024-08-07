#!/usr/bin/env python
#!/usr/bin/python3

import argparse
import ipaddress
import os
import socket
import struct
import threading
import time
from typing import Union

# HEX_FILTER string containing ASCII printable characters (if one exists) or a dot if representation does not exist.
#   - the representation of the printable character has a length of 3
#   - breakdown:
#       - For each integer in range 0-256, if the length of the corresponding character equals 3,
#         we get the character (chr(i)), otherwise we get a dot ('.').
#         Then join that list into a string to look like:
#         ................................ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[.]^_`abcdefghijklmnopqrstuvwxyz{|}~..................................¡¢£¤¥¦§¨©ª«¬.®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

class IP:
    """
    IP class that can read a packet and parse the header into it's own separate fields (map the first 20 bytes of the received buffer into a friendly IP header).

    Keyword Arguments:
    - buff (string): packet data

    Example:
    mypacket = IP(buff)
    print (f'{mypacket.src_address} -> {mypacket.dst_address}')
    """
    def __init__(self,buff=None):
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
            err_msg = ("%s No protocol for %s" % (e, self.protocol_num))
            print(err_msg)
            self.protocol = str(self.protocol_num)

    def __str__(self) -> str:
        return f"{self.src_address} -> {self.dst_address}"

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
    def __init__(self, host:str=None, subnet:str=None, verbose_mode:bool=False):
        self.host = get_ip_address() if host is None else host
        self.subnet = get_subnet(self.host) if subnet is None else subnet
        print(f"running scanner on host {self.host} ({self.subnet})")

        socket_protocol = socket.IPPROTO_IP if (os.name=='nt') else socket.IPPROTO_ICMP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((self.host, 0))

        # set sock option to include the IP header in the captured packets
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        print('Hitting promiscuous mode.')
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self, message:str="ACK!"):
        """
        Similar to main sniffer method, but keeps track of which hosts are up.
        If the anticipated ICMP message is detected:
            - check that the ICMP response is coming from within the target subnet
            - has the message string in it
        """
        hosts_up = set([f'{str(self.host)} *'])
        try:
            while True:
                print('.',end='')
                raw_buffer = self.socket.recvfrom(65535)[0]
                ip_header = IP(raw_buffer[0:20])
                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    icmp_header = ICMP(buf)

                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(self.subnet):
                            if raw_buffer[len(raw_buffer) - len(message): ] == bytes(message, 'utf-8'):
                                hosts_up.add(str(ip_header.src_address))
                                print(f"Host Up: {str(ip_header.src_address)}")
        # handle CTRL-C
        except KeyboardInterrupt:
            if  os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

            print('\nUser interrupted.')
            if hosts_up:
                print(f'\n\nSummary: Hosts up on {self.subnet}')
            for host in sorted(hosts_up):
                print(f'{host}')
            print('')
            sys.exit()
        except Exception as e:
            print (f"ERROR: {e.__str__()}")
        return

def ip2long(ip:str)->int:
    packed = socket.inet_aton(ip)
    lng = struct.unpack("!L", packed)[0]
    return lng

def long2ip(lng:int)->str:
    packed = struct.pack("!L", lng)
    ip = socket.inet_ntoa(packed)
    return ip

def get_ip_address():
    """
    Creates UDP socket to retrieve IP (eth0) address.

    src: https://stackoverflow.com/a/30990617/14745606
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0] or None

def get_subnet(host:str=None, subnet_mask:str="255.255.255.0"):
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

def hexdump(data:Union[str,bytes], length:int=16, show:bool=True)->list[str]:
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
    if show:
        for line in results:
            print(line)
    return results

def scan_port(ip_address:str, port:int, timeout:int=None, send_packet:bool=False):
    """
    src: https://www.geeksforgeeks.org/python-simple-port-scanner-with-sockets/#
    src: https://www.geeksforgeeks.org/how-to-get-open-port-banner-in-python/
    """
    ip_address = socket.gethostbyname(socket.gethostname()) if ip_address is None else ip_address
    packet = b"\x47\x45\x54\x20\x2f\x20\x48\x54\x54\x50\x2f\x31\x2e\x30\x2e\x2e\x2e\x2e"
    try:
        # create socket object with:
        #   - AF_INET -> using standard IPv4 address or hostname
        #   - SOCK_STREAM -> TCP client
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if timeout is not None: s.settimeout(timeout)
        s.connect((ip_address, port))
        if send_packet: s.send(packet)

        # try getting banner
        try:
            banner = s.recv(1024).decode()
            print (f"port {port} is open with banner ({len(banner)}): {banner}")
        except:
            print (f"port {port} is open.")
    except:
        print (f"port {port} is closed")
        pass

def sniffer(ip_address:str=None):
    """
    Packet sniffing on Windows and Linux machines.
    Note: may need to run with sudo privileges

    Keyword Arguments:
    ip_address (str): ip address of machine to sniff

    """
    ip_address = ip_address or get_ip_address()
    os_name = os.name
    print(f"Starting packet sniffer on {ip_address} - {os_name}")
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
            ip_header = IP(raw_buffer[0:20])
            print(f"IP Header: {ip_header.protocol}\t{ip_header}")
            print(f'Version: {ip_header.ver} Header Length: {ip_header.ihl}  TTL: {ip_header.ttl}')
            if ip_header.protocol == 'ICMP':
                # calculate the offset in the raw packet where ICMP body lives
                offset = ip_header.ihl * 4
                buf = raw_buffer[offset:offset + 8]
                icmp_header = ICMP(buf)
                print(f"ICMP -> Type: {icmp_header.type} Code: {icmp_header.code}\n")

    except KeyboardInterrupt:
        # if on Windows, turn off promiscuous mode
        if os_name == 'nt': sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
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
    import paramiko
    #   - note: Paramiko also supports auth w/ keys instead of password auth
    # TODO:
    #   - utilize using keys
    #   - modify to run multiple commands on SSH server
    #   - run commands on multiple SSH servers.

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
    import sys
    def get_args():
        list_of_choices = [
            'get_ip_address',
            # 'get_subnet',
            # 'udp_sender',
            'hexdump',
            'scanner',
            'scan_port',
            'sniffer',
        ]
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
    debug = args.get('debug', False)
    if debug:
        print (f"args ({type(args)}): {args} ")
        print (f"action: {action}")
        print (f"data: {data}")
        print ("-"*50 + "\n")

    results = ""
    if action == 'get_ip_address':
        results = get_ip_address()
        print (f"\n{results}\n")

    elif action == 'hexdump':
        results = hexdump(data)

    elif action == 'scan_port':
        host_ip = get_ip_address()
        start_time = time.time()

        # todo: if no port specified, scan all the ports
        for i in range(0, 100000):
            thread = threading.Thread(target=scan_port, args=[host_ip, i])
            thread.start()
        end_time = time.time()
        print (f"To scan all ports it took {end_time-start_time} seconds")

    elif action == 'sniffer':
        # sudo python3 ./network.py sniffer -d --data "192.168.0.207"
        ip_address = data or get_ip_address()
        sniffer(ip_address)

    elif action == 'scanner':
        # sudo python3 network.py scanner
        ip_address = data or get_ip_address()
        message : str = sys.argv[2] if len(sys.argv) >= 3 else 'ACK!'
        print (f"using message: {message}")
        scanner = Scanner(ip_address, verbose_mode=debug)
        time.sleep(10)
        t = threading.Thread(target=udp_sender, args=[scanner.subnet,message])
        t.start()
        scanner.sniff(message=message)
    else:
        print("Unknown action.")
        sys.exit(1)
