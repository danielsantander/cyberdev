*Python Scripts Table of Contents*
- [cleanup.py](#cleanuppy)
- [encryptPDF.py](#encryptpdfpy)
- [netcat.py](#netcatpy)
  - [Setup Lister and Client](#setup-lister-and-client)
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
