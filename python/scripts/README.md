*Python Scripts Table of Contents*

- [cleanup.py](#cleanuppy)
- [encryptPDF.py](#encryptpdfpy)
- [netcat.py](#netcatpy)
  - [Setup Lister and Client](#setup-lister-and-client)
- [pollen8.py](#pollen8py)
  - [Pollen8 Usage](#pollen8-usage)
  - [Module Examples](#module-examples)
  - [Scan](#scan)
  - [Sniffer](#sniffer)
    - [Packet Sniffing](#packet-sniffing)
  - [SSH Commands](#ssh-commands)
    - [Single Command](#single-command)
    - [SSH Client/Server Setup](#ssh-clientserver-setup)
- [proxy.py](#proxypy)
- [rename\_files.py](#rename_filespy)
- [SSH](#ssh)
  - [ssh\_cmd](#ssh_cmd)
  - [SSH client and server](#ssh-client-and-server)

---

# cleanup.py

Will iterate through the given source directory to consolidate files into their own sub-directories, such as:
    - screenshots/
    - {extension name}/, such as:
      - PDFs/
      - PNG/
      - JPEG/

Usage: `./cleanup.py <source directory path> <destination directory path [OPTIONAL]>`

Example:

```shell
./cleanup.py /home/ /home/results/
```

# encryptPDF.py

Python script for encrypting PDF files.

Usage: `./encryptPDF [PDF file] [output location]`

> pw defaults to 'fairbanks' if not given when prompted

**Example**: Encrypt `tests/sample_test_data/pdfs/HelloWorld.pdf` and output the encrypted file in the same directory as the file to encrypt.
There should then be an encrypted PDF file located at `tests/sample_test_data/pdfs/HelloWorldENCRYPTED.pdf` (outputs in same directory as the input file).

```shell
./encryptPDF.py tests/sample_test_data/pdfs/HelloWorld.pdf
```

**Example**: Encrypt the same PDF file, but send output to the current directory.
There should then be an encrypted PDF file located in the current directory named `HelloWorldENCRYPTED.pdf`.

```shell
./encryptPDF.py tests/sample_test_data/pdfs/HelloWorld.pdf .
```

# netcat.py

A simple network client and server to push files, or act as a listener to provides command line access.

Usage:

```shell
./netcat.py -h
usage: netcat.py [-h] [-c] [-e EXECUTE] [-l] [-p PORT] [-t TARGET] [-u UPLOAD]

Network client server tool

optional arguments:
  -h, --help            show this help message and exit
  -c, --command         command shell
  -e EXECUTE, --execute EXECUTE
                        execute specified command
  -l, --listen          listen
  -p PORT, --port PORT  specified port
  -t TARGET, --target TARGET
                        specified IP
  -u UPLOAD, --upload UPLOAD
                        upload file

Example:
                                      netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
                                      netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload file
                                      netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd" # execute command
                                      echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
                                      netcat.py -t 192.168.1.108 -p 5555 # connect to server
```

## Setup Lister and Client

On a machine setup a listener using its own IP and port 5555 to provide a command shell.

```shell
python3 netcat.py -t {ip_address} -p 5555 -l -c
```

On another within another machine's terminal run in client mode.

> script reads from stdin and will do so until the end-of-file (EOF) marker.

```shell
python3 netcat.py -t {listener_ip_address} -p 5555

CTRL-D
<NETCAT:#>  ls -la
```

# pollen8.py

Script that does some neat network stuff in Python.

## Pollen8 Usage

```shell
python3 pollen8.py -h
usage: pollen8.py [-h] [-d] [-p PORT] [--ssh-server [IP PORT ...]] [--ssh-client [IP PORT ...]]
                  [--ssh-cmd IP PORT [IP PORT ...]] [--sniff [IP_ADDRESS/CIDR ...]] [--scan]

Pollen8 -- Script that does some neat network stuff.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Debug mode. Defaults to False
  -p PORT, --port PORT  Port value.
  --ssh-server [IP PORT ...]
                        Create SSH server. Input server ip address & port as arguments.
  --ssh-client [IP PORT ...]
                        Create SSH client. Input server IP address as argument.
  --ssh-cmd IP PORT [IP PORT ...]
                        Make connection to SSH server and run single command
  --sniff [IP_ADDRESS/CIDR ...]
                        Sniff network packet data.
  --scan                Scan local network.

Example:
    --ssh-server <ip_address> <port_number>
    --ssh-client <ip_address> <port_number>
    --ssh-cmd <ip_address> <username> <command> <port_number>
    --sniff
    --scan
```

## Module Examples

```python
from pollen8 import Pollen8
p = Pollen8()
p.host.ip_address
p.host.hostname
p.subnet

# Scan a target's port for banner
# returns tuple (str,bool) => (True if port open else False, 'BANNER MESSAGE HERE, IF FOUND')
p.check_port(ip_address=p.host.ip_address, port=80)

# Scan multiple ports on target
p.scan_target(ip_address=p.host.ip_address, port_list=[22, 80])

# Send TCP message to target host and port
p.tcp_client(target_host="10.0.0.10", port=22, message=b"GET / HTTP/1.1\r\n")

# Start up a standard multi-threaded TCP server/listener
p.tcp_server(port=4444, response_message=b'rgr')

# Send UDP message to target host and port.
# Will wait for response back (timeout defaults to 5s)
p.udp_client(target_host="10.0.0.10", port=4444, message=b'ACK')

# Connect to SSH server and run single command, returns list of responses.
p.ssh_cmd('10.0.0.10', 'root', 'password123', 'whoami')
['root\n']

# Create SSH server for a client to connect to.
p.ssh_server(port=2222)
```

## Scan

Host discovery scan covering a whole subnet. Trigger with `--scan` option. Exit script loop with `^C`.

> note: this script utilizes promiscuous mode, requiring admin privileges on Windows or root on Linux. This allows sniffing of all packets that the network card sees. May need to use with `sudo`.

```shell
sudo python3 pollen8.py --scan
Password:
2024-08-13 23:41:38,940 [INFO] NETWORK: running scanner on host 10.0.0.10 (10.0.0.0/24)
.++++++++++.+++++.+++++.++++++++++++.++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++Host Up: 10.0.0.100
^C2024-08-13 23:51:15,561 [INFO] Scanner:
User interrupted.
.++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Summary: Hosts up on 10.0.0.0/24
10.0.0.10 *
10.0.0.100
```

## Sniffer

Uses raw sockets to read low level network data (IP/ICMP headers). Run with the following command:

```shell
python3 pollen8.py --sniff
```

To test, within another terminal ping google `ping google.com`, then in the original terminal, see the  decoded IP headers from the captured packets:

```shell
2024-01-31 01:13:28,498 [INFO] Pollen8: Starting sniffer on 10.0.0.10 . . .
Protocol: ICMP 142.251.116.138 -> 10.0.0.10
Version: 4
Header Length: 5 TTL: 105
ICMP -> Type: 0 Code: 0

Protocol: ICMP 142.251.116.138 -> 10.0.0.10
Version: 4
Header Length: 5 TTL: 105
ICMP -> Type: 0 Code: 0

Protocol: ICMP 142.251.116.138 -> 10.0.0.10
Version: 4
Header Length: 5 TTL: 105
ICMP -> Type: 0 Code: 0
```

### Packet Sniffing

Windows machines require additional flags for socket input/output control (IOCTL) to enable promiscuous mode on the network interface.

Windows will allow sniffing of all incoming packets regardless of protocol, whereas Linux requires sniffing of ICMP packets.

## SSH Commands

### Single Command

USAGE: `./pollen8.py --ssh-cmd {IP_ADDRESS} {USERNAME} {COMMAND} {PORT}`

```shell
./pollen8.py --ssh-cmd {IP_ADDRESS}

Starting SSH command...
User: root
Password: password123!
command: whoami
--- OUTPUT ---
root

# may also add username and command into args:
python3 pollen8.py --ssh-cmd {IP_ADDRESS} root "whoami"

Starting SSH command...
Password:
--- OUTPUT ---
root
```

### SSH Client/Server Setup

On Machine-A start a SSH server and begin listening:

```shell
python pollen8.py --ssh-server {SERVER_IP_ADDRESS} 2222
2024-01-22 23:48:25,252 [INFO] Pollen8: ssh_server: starting SSH server on {SERVER_IP_ADDRESS}, 2222...
2024-01-22 23:48:25,325 [INFO] Pollen8: [+] Listening for connection ...
```

On Machine-B create the SSH client:

```shell
python3 pollen8.py --ssh-client {SERVER_IP_ADDRESS}
User [root]:
Password:
2024-01-22 23:48:32,374 [INFO] Pollen8: ssh_rcmd: starting ssh client on {SERVER_IP_ADDRESS}, 2222
Welcome to Pollen8 SHH server.
```

Then back on Machine-A (the SSH server), you can enter commands to run on the client.

```shell
2024-01-22 23:48:32,649 [INFO] Pollen8: [+] Got a connection! <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('{SERVER_IP_ADDRESS}', 2222), raddr=('{CLIENT_IP_ADDRESS}', {CLIENT_PORT})> ('{CLIENT_IP_ADDRESS}', CLIENT_PORT)
2024-01-22 23:48:32,875 [INFO] Pollen8: [+] Authenticated
2024-01-22 23:48:32,883 [INFO] Pollen8: ClientConnected
Enter command: pwd
--- OUTPUT ---
/home/root/

Enter command:
```

# proxy.py

TCP proxy

Usage: `./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]`

Example -- run proxy against FTP server

```shell
# fire up proxy w/ sudo bc port 21 is a privileged port
sudo python3 proxy.py {ftp_server_ip_address} 21 ftp.sun.ac.za 21 True
```

In another terminal, start a FTP session using default port 21

```shell
sudo ftp {ftp_server_ip_address}
```

# rename_files.py

run in debug mode:

```shell
./rename_files.py <filepath> -i --debug --preface="preface_filename_with_this__"
```

# SSH

The `Paramiko` library is used in these scripts to utilize raw sockets in order to create SSH clients/servers. Install Paramiko library if necessary:

```shell
python3 -m pip install paramiko
```

## ssh_cmd

Tunnel traffic using a secure shell (SHH). Encrypt traffic to help avoid detection. However, a lot of clients do not provide a SSH client (such as most Window systems, however PuTTY may be available).

Example -- Make SSH connection and run single command on server.

```shell
python3 ssh_cmd.py
Username: admin
Password:
Enter server IP: {enter_server_ip_address}
Enter port or [22]: {enter_server_port}
Enter command or [id]: {enter_command_to_run}
--- Output ---
uid=1000(admin) gid=1000(admin) groups=1000(admin),27(sudo)
```

## SSH client and server

**ssh_rcmd.py** is a modification of `ssh_cmd.py` script to run commands on the Windows client over SSH.

Because most versions of Microsoft Windows don't include a SSH server (out of the box), we need to reverse and send commands from a SSH server to the SSH client. This script will act as the client to the server.

**ssh_server.py** is a script to create a SSH server that will listen for the client started by ssh_rcmd.

Example:

Run server on MacOS

```shell
sudo python3 ssh_server.py
Password:
Enter server IP: {SERVER_IP_ADDRESS}
Enter port [2222]:
starting ssh server:	{SERVER_IP_ADDRESS}, 2222
[+] Listening for connection ...
```

Then on Windows machine, run the client script:

```shell
sudo python3 ssh_rcmd.py
Password:
Enter server IP: {SERVER_IP_ADDRESS}
Enter port [2222]:
Welcome to SHH server
```

Back on the Mac SSH server, output should now be:

```shell
[+] Got a connection! <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('{SERVER_IP_ADDRESS}', 2222), raddr=('{CLIENT_IP_ADDRESS}', 54255)> ('{CLIENT_IP_ADDRESS}', 54255)
[+] Authenticated
ClientConnected
Enter command:
```
