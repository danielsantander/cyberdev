#!/usr/bin/env python
#!/usr/bin/python3

import ipaddress
import socket
import time

def get_ip_address():
    """
    Retrieve IP address (eth0 address) by creating UDP socket.

    src: https://stackoverflow.com/a/30990617/14745606
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

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