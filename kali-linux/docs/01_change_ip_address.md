# Change Your IP Address
Use the `ifconfig` command as shown:

```bash
ifconfig <interface> <new_ip_address>
```

*Example:*
```bash
ifconfig eth0 192.168.180.115
```

# Change Network Mask and Broadcast

You can also use the `ifconfig` command to change the network mask (netmask) and broadcast address.

```bash
ifconfig eth0 192.168.180.115 netmask 255.255.0.0 broadcast 192.168.1.255
```