# Change/Spoof MAC Address
Use the `ifconfig` command and perform the following to change the MAC address:
1. Use the `down` option to take down the interface (eth0 in this case)
2. Change the MAC Address
3. Bring up the interface with the `up` option

eth0 Example:
```bash
root@kali:~# ifconfig eth0 down
root@kali:~# ifconfig eth0 hw ether 00:11:22:33:44:55
root@kali:~# ifconfig eth0 up
```

wlan0 Example
```bash
root@kali:~# ifconfig wlan0 down
root@kali:~# ifconfig wlan0 hw ether 00:11:22:33:44:55
root@kali:~# ifconfig wlan0 up

```

