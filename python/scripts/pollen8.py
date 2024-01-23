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
import logging
import paramiko
import os
import socket
import sys
import threading

DEBUG_MODE = False
CWD = os.path.dirname(os.path.realpath(__file__))

# debug paramiko
logging.getLogger("paramiko").setLevel(logging.DEBUG)

def get_args():
    import textwrap
    parser = argparse.ArgumentParser(
        description="Pollen8 -- Script that does some neat network stuff.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            --ssh-server 192.168.0.100 2222
            --ssh-client 192.168.1.100
            --ssh-cmd 192.168.1.100 root "whoami" 22
        '''))
    parser.add_argument('-d', '--debug',
        dest='debug',
        action='store_true',
        default=DEBUG_MODE,
        help=f'Debug mode. [{DEBUG_MODE}]')

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
    args = parser.parse_args()
    return args

def setup_logger(name:str=None, debug_mode:bool=DEBUG_MODE):
    """
    setup logger
    """
    lgr_lvl = logging.DEBUG if debug_mode else logging.INFO
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

class Pollen8:
    def __init__(self, **kwargs):
        self.logger = setup_logger("Pollen8")

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
    args = get_args()
    if args.debug:
        print("DEBUG MODE")
        sys.exit(0)

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

    else:
        print("no action")
        sys.exit()

if __name__ == '__main__':
    main()