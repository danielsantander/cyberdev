#!/usr/bin/env python
#!/usr/bin/python3

"""
example:
python3 ssh_cmd.py
Username: admin
Password:
Enter server IP: 192.168.0.10
Enter port or <CR>: 22
Enter command or <CR>: id
--- Output ---
uid=1000(tim) gid=1000(tim) groups=1000(tim),27(sudo)

example 2:
(.djs) santander-2:scripts santander$ ./ssh_cmd.py
Username: pi
Password:
Enter server IP: 192.168.0.100
Enter port or <CR>: 22
Enter command or <CR>: cd /home/pi/code/repos/cyberdev/kali-linux/scripts/; ./nmap_active_devices_on_network.sh 192.168.0.100/24;
--- OUTPUT ---

performing nmap (sP scan) on 192.168.0.100/24 ...

--------------------
IP ADDRESSES FOUND:
--------------------
192.168.0.1
192.168.0.2
192.168.0.8
192.168.0.16
192.168.0.29
192.168.0.100

"""

import paramiko

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

if __name__ == '__main__':
    import getpass
    user = input('Username: ')
    passwd = getpass.getpass()

    ip = input('Enter server IP: ')
    assert(ip)
    port = input('Enter port [22]: ') or 22
    cmd = input('Enter command or [id]: ') or 'id'
    ssh_command(ip, port, user, passwd, cmd)


