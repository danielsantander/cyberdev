- [Install Drivers](#install-drivers)
  - [RealTek ALFA AWUS036ACS](#realtek-alfa-awus036acs)
- [Metasploit](#metasploit)
  - [wmap](#wmap)

```shell
apt update && apt full-upgrade -y

# search for package modules installed
apt-cache search {package}
```

# Install Drivers

## RealTek ALFA AWUS036ACS

This is the process in which to install the ALFA AWUS036ACS drivers on Kali Linux 2020.

```shell
# install drivers
sudo apt-get install realtek-rtl88xxau-dkms

# install Dynamic Kernel Module Support (dkms)
sudo apt-get install dkms

# clone drivers from aircrack-ng github page
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au/

# install software
make
sudo make install

#------------------
# troubleshooting
#------------------
# if 'no such file or directory' error performing make, try installing the linux headers:
sudo apt-get install linux-headers-$(uname -r)

# or maybe:
sudo apt-get install build-essential linux-headers-$(uname -r)

# show usb and wifi config
lsusb
iwconfig
```

You may need to uninstall and purge wifi drivers and then reinstall it using the following commands below.

```shell
# install driver
sudo apt install realtek-rtl88xxau-dkms

# uninstall & purge
apt remove realtek-rtl88xxau-dkms
apt purge realtek-rtl88xxau-dkms
```

# Metasploit

```shell
# open Metasploit
msfconsole

# open Metasploit without header
msfconsole -q

# ensure postgresql is started
sudo service --status-all | grep "postgresql"
sudo service postgresql start

```

## wmap

wmap utility will scan a list of URLs to test whether the web server exhibits security flaws.

> Ensure you run the utility on a website you own.

```shell
# load wmap framework plugin
msf6> load wmap

# run against a target
msf6> wmap_targets -t https://0.0.0.0
```
