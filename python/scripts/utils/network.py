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
        results.append(f'{i:04x}  {hexa:<{hexwidth}}  {printable}')
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

    # return one packet
    packet = sniffer.recvfrom(65565)
    print(f"packet:\n{packet}")

    # if on Windows, turn off promiscuous mode
    if os_name == 'nt': sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    return packet


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
    Sends UDP datagrams to all IP address in given subnet.
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
            'scan_port',
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

        print (f"To all scan all ports it took {end_time-start_time} seconds")
    else:
        sys.exit(1)
