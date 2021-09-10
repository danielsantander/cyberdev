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



