# Mapping IP Addresses

Locate the host file at `/etc/hosts`.

Here you can set specific IP address-domain name mapping which will determine which IP address your browsers directs to given a specific domain name.

```shell
root@kali:~# cat /etc/hosts
127.0.0.1       localhost
127.0.1.1       kali

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```
