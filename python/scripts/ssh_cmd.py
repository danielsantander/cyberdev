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
./ssh_cmd.py
Username: root
Password:
Enter server IP: 192.168.0.100
Enter port or <CR>: 22
Enter command or <CR>: cd /home/root/scripts/; ./nmap_active_devices_on_network.sh 192.168.0.100/24;
--- OUTPUT ---

performing nmap (sP scan) on 192.168.0.100/24 ...

--------------------
IP ADDRESSES FOUND:
--------------------
192.168.0.1
...
192.168.0.100
"""

import paramiko
from utils.network import ssh_command

if __name__ == '__main__':
    import getpass
    user = input('Username: ')
    passwd = getpass.getpass()

    ip = input('Enter server IP: ')
    assert(ip)
    port = input('Enter port [22]: ') or 22
    cmd = input('Enter command or [id]: ') or 'id'
    ssh_command(ip, port, user, passwd, cmd)


