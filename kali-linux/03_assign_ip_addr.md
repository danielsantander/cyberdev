# Assign IP Address From DHCP Server
The DHCP server assignes IP addresses to all systems on the subnet, with logs of which ip address is assigned to which machine.

You can request an IP address from the DHCP by calling the DHCP server with the `dhclient` command followed by the interface you want the address assigned to.

```bash
root@kali:~# dhclient <interface>
```

**eth0 example**
```bash
root@kali:~# ifconfig dhclient eth0
```

**wlan0 example**
```bash
root@kali:~# ifconfig dhclient wlan0
```

<br>
<hr>
<br>

## Trouble Shooting
```
root@kali:~# dhclient wlan0
root@kali:~# RTNETLINK answers: File exists
```

*Fix found from [serverfault.com](https://serverfault.com/questions/601450/dhclient-what-does-rtnetlink-answers-file-exists-mean)*

Suggested by user "Dennis Nolte":

You 
For having the lease renewed do
```
dhclient -r
```

If thats not enough you can remove all leases by removing the file and getting a new lease
```
sudo rm /var/lib/dhcp/dhclient.leases; sudo dhclient eth0
```
Depending on your exact setup this might be an issue with having to type your password twice, so watch out for that.


