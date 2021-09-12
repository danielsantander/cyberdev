# Kali Linux Tips & Scripts

Any tips or notes are written in markdown files (`.md` extension) and any executable scripts will be written in shell script files (`.sh`).

Script files will begin with the shebang: `#!/bin/bash`


## Useful Tips

### Check Kali Linux Version
```bash
$ lsb_release -a
```

### Check Wireless Network Devices
Utilize the `iwconfig` command to gather information such as the wireless adapter's IP addres, MAC address, what mode it is in, and much more.

```shell
$ iwconfig
wlan0 IEE 802.11bg SSID:off/any
Mode:Managed Access Point: Not Associated Tx-Power-20 dBm
--snip--
lo      no wireless connection
eth0    no wireless connection
```

### Print Random Line From File
Using the `shuf` utility, print random lines from a file. 
Use the `-n` flag to determine the number of lines to output.
```bash
$ shuf -n 1 <filename>
```
