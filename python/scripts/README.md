*Python Scripts Table of Contents*

- [cleanup.py](#cleanuppy)
- [encryptPDF.py](#encryptpdfpy)
- [netcat.py](#netcatpy)
  - [Setup Lister and Client](#setup-lister-and-client)
- [pollen8.py](#pollen8py)
  - [Sniffer](#sniffer)
    - [Discover Active Hosts On Network](#discover-active-hosts-on-network)
    - [Packet Sniffing](#packet-sniffing)
    - [Scanner](#scanner)
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
    - <extension name>
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

**Example**: Encrypt `tests/sample_data/pdfs/HelloWorld.pdf` and output the encrypted file in the same directory as the file to encrypt.
There should then be an encrypted PDF file located at `tests/sample_data/pdfs/HelloWorldENCRYPTED.pdf` (outputs in same directory as the input file).

```shell
$ ./encryptPDF.py tests/sample_data/pdfs/HelloWorld.pdf
```

**Example**: Encrypt the same PDF file, but send output to the current directory.
There should then be an encrypted PDF file located in the current directory named `HelloWorldENCRYPTED.pdf`.

```shell
./encryptPDF.py tests/sample_data/pdfs/HelloWorld.pdf .
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

## Sniffer

Uses raw sockets to read low level network data:

- Internet Protocol (IP) headers
- Internet Control Message Protocol (ICMP) headers

> TODO: decode Ethernet information. Use Ethernet frames and their use, such as:
>
> - ARP poisoning
> - wireless assessment tools

Run:

```shell
python3 pollen8.py --sniff
2024-01-30 23:46:36,153 [INFO] Pollen8: Starting scan on santander-2.local ({host_ip_address})...
```

In another terminal, ping google:

```shell
ping google.com
```

In the original terminal, see the  decoded IP headers from the captured packets:

```shell
2024-01-30 23:46:36,153 [INFO] Pollen8: Starting scan on 192.168.0.7 . . .
Protocol: ICMP 142.250.138.101 -> 192.168.0.7
Protocol: ICMP 142.250.138.101 -> 192.168.0.7
Protocol: ICMP 142.250.138.101 -> 192.168.0.7

```

### Discover Active Hosts On Network

Main goal of sniffer is to discover hosts on a target network.

Attackers want to see potential all of the targets on a network so they can focus their reconnaissance and exploitation attempts.

- Determine if there is an active host at a particular IP address.
  - When sending a UDP datagram to ta closed port on a host the host typically sends back an ICMP message indicating that the port is unreachable.
    - This ICMP message tells s that there is a host alive, because if there no host, we probably wouldn't receive a response to the UDP datagram.
      - Therefore, pick a UDP port that won't likely be used (for maximum coverage, we can probe several ports to ensure we aren't hitting an active UDP service)
    - Why use UDP -> not a lot of overhead sending UDP messages across a subnet.
      - Really a simple scanner to build

> TODO: implement logic in scanner to kick off full Nmap port scans on any hosts we discover
>   - used to determine a viable network attack surface

### Packet Sniffing

Windows machines require additional flags for socket input/output control (IOCTL) to enable promiscuous mode on the network interface.

**Input/Output Control (IOCTL)** means for user spce programs to communicate with kernel mode components [src](http://en.wikipedia.org/wiki/Ioctl).

Windows will allow sniffing of all incoming packets regardless of protocol, whereas Linux requires sniffing of ICMP packets.

### Scanner

> note this script utilizes promiscuous mode, requiring admin privileges on Windows or root on Linux. This allows sniffing of all packets that the network card sees.

```shell
sudo ./pollen8.py [IP_ADDRESS/CIDR]
```

Then in another terminal, make a ping.

```shell
ping google.com
```

The sniffer terminal should now show results:

```shell
sudo ./pollen8.py --scan 192.168.0.100/24
(b'E\x00@\x00\x00\x00\x00\x00i\x01\x8f\x98\x8e\xfarf\xc0\xa8\x00\x08\x00\x00*\x1f\x1fM\x00\x00e\xb4_\xdd\x00\x07\x05\xf8\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567', ('142.250.114.102', 0))
```

## SSH Commands

### Single Command

USAGE: `./pollen8 --ssh-cmd {IP_ADDRESS} {USERNAME} {COMMAND} {PORT}`

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
