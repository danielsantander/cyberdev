# Change DNS Server


Locate the plain text file `/etc/resolv.conf`

```shell
root@kali:~# cat /etc/resolv.conf 
domain localdomain
search localdomain
nameserver 198.168.180.10
```

The nameserver is set to local DNS server located at `198.168.180.10`

Change the nameserver value to add Google's public DNS server (`8.8.8.8`)

`/etc/resolv.conf`
```shell
root@kali:~# echo "nameserver 8.8.8.8" > /etc/resolv.conf 
root@kali:~# cat /etc/resolv.conf 
nameserver 8.8.8.8
```

The machine will now go out to Google's DNS server rather than the initial local DNS server to resolve the domain names into IP addresses.


## Regenerate `resolv.conf`

```shell
sudo resolvconf -u
```

### Install and start resolvconf service.

```shell
root@kali:~# sudo apt install resolvconf
```

After install, enable and run the service.

```shell
root@kali:~# systemctl enable resolvconf.service
Synchronizing state of resolvconf.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable resolvconf
Created symlink /etc/systemd/system/sysinit.target.wants/resolvconf.service → /lib/systemd/system/resolvconf.service.
root@kali:~# systemctl start resolvconf.service
root@kali:~# systemctl status resolvconf.service
● resolvconf.service - Nameserver information manager
     Loaded: loaded (/lib/systemd/system/resolvconf.service; enabled; vendor preset: disabled)
     Active: active (exited) since Fri 2021-09-10 18:10:11 CDT; 9s ago
       Docs: man:resolvconf(8)
    Process: 1915 ExecStart=/sbin/resolvconf --enable-updates (code=exited, status=0/SUCCESS)
   Main PID: 1915 (code=exited, status=0/SUCCESS)

Sep 10 18:10:11 kali systemd[1]: Started Nameserver information manager.
```

Check status of `resolv.conf` file


