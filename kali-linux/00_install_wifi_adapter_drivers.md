# Install Drivers
This is the process in which to install the ALFA AWUS036ACS drivera on Kali Linux 2020

[Source](https://www.kryptostechnology.com/alfa-awus036acs-driver-install-kali-linux/)

## Uninstall and Purge

The Driver is preinstalled with the Kali Linux Kernel, so there is not much to do, so first, you will need to uninstall and purge wifi drivers and then reinstall it using the following commands below.

```shell
$ apt-get remove realtek-rtl88xxau-dkms
$ apt-get purge realtek-rtl88xxau-dkms
```
## Re-install

```shell
$ apt-get install realtek-rtl88xxau-dkms
```
