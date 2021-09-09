# Assign IP Address From DHCP Server
The DHCP server assignes IP addresses to all systems on the subnet, with logs of which ip address is assigned to which machine.

You can request an IP address from the DHCP by calling the DHCP server with the `dhclient` command followed by the interface you want the address assigned to.

```bash
root@kali:~# dhclient <interface>
```

**eth0 example**
```bash
root@kali:~# dhclient eth0
```

**wlan0 example**
```bash
root@kali:~# dhclient wlan0
```

<br>
<hr>
<br>

## Trouble Shooting
```
root@kali:~# dhclient wlan0
root@kali:~# RTNETLINK answers: File exists
```

*Fix found from [serverfault.com](https://serverfault.com/questions/601450/dhclient-what-does-rtnetlink-answers-file-exists-mean)* - (suggested by user Dennis Nolte)

Release  the  current  lease  and  stop the running DHCP client as previously recorded in the PID file.
```shell
dhclient -r
```

Another solution would be to remove all leases by removing the file and getting a new lease.
```shell
root@kali:~# sudo rm /var/lib/dhcp/dhclient.leases
root@kali:~# sudo dhclient eth0
```
