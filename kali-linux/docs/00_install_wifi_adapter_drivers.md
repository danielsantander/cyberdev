- [Install Drivers](#install-drivers)
  - [Uninstall and Purge](#uninstall-and-purge)
  - [Install](#install)

# Install Drivers

This is the process in which to install the ALFA AWUS036ACS drivers on Kali Linux 2020

[Source](https://www.kryptostechnology.com/alfa-awus036acs-driver-install-kali-linux/)

## Uninstall and Purge

The Driver is preinstalled with the Kali Linux Kernel, so there is not much to do, so first, you will need to uninstall and purge wifi drivers and then reinstall it using the following commands below.

```shell
apt-get remove realtek-rtl88xxau-dkms
apt-get purge realtek-rtl88xxau-dkms
```

## Install

```shell
# install drivers
sudo apt-get install realtek-rtl88xxau-dkms

# install dkms
sudo apt-get install dkms

# clone drivers from aircrack-ng github page
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au/

# install software
make
sudo make install
```

> note: if `no such file or directory` error performing `make`, try installing the linux headers:
>
> ```shell
> sudo apt-get install linux-headers-$(uname -r)
>
> # or maybe:
> sudo apt-get install build-essential linux-headers-$(uname -r)
>
> # show usb and wifi config
> lsusb
> iwconfig
> ```
