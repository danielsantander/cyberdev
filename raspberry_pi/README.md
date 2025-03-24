*Table of Contents*
- [Download Raspberry Pi OS](#download-raspberry-pi-os)
- [Update and Upgrade System](#update-and-upgrade-system)
- [View OS Info](#view-os-info)
- [compress/uncompress](#compressuncompress)
- [cron](#cron)
- [Mounting/Unmounting Devices](#mountingunmounting-devices)
- [Install Software](#install-software)
  - [Docker](#docker)
    - [Troubleshoot](#troubleshoot)
  - [Picamera](#picamera)
- [raspi-config](#raspi-config)
  - [Boot Raspberry Pi to Desktop GUI](#boot-raspberry-pi-to-desktop-gui)
  - [Disable Screen Blanking](#disable-screen-blanking)
- [Tips](#tips)
  - [Disable or Extend Sleep on Raspberry Pi](#disable-or-extend-sleep-on-raspberry-pi)

---

# Download Raspberry Pi OS

Download Raspberry Pi Operating Systems here: https://www.raspberrypi.com/software/operating-systems/

# Update and Upgrade System

```shell
sudo apt-get update && sudo apt-get upgrade -y
```

# View OS Info

```shell
# view os
cat /etc/os-release

# check linux version
lsb_release -a

# view bit size
uname -m
# Output Expected:
# - aarch64 (for 64 bit)
# - armv7l (for 32 bit)
```

# compress/uncompress

```shell
# compress directory of data into a tar
tar -cvf archive.tar data/

# compress into gzip
tar -czvf archive.tar.gz data/

# extract files from tarball
tar -xvf archive.tar

# compress using gzip -- data.tar -> data.tar.gz
gzip data.tar

# decompress tar.gz and .tgz files -- data.tar.gz -> data.tar
gunzip data.tar.gz

```

# cron

`/etc/crontab` is the system wide crontab, whereas `crontab -e` is per user. Specify which user with `crontab -e -u <username>`

# Mounting/Unmounting Devices

Mount points -- locations in the directory tree where the devices area attached to. Two main mount points in Linux are:

1. `/mnt`: Usually used to mount internal hard drives.
2. `/media`: Usually used to mount external USB devices (flash drives) and external USB hard drives.

> Can not unmount a device that is busy, that is if the system is busy reading or writing data to the storage device.

```shell
# mount a `sbd1` hard drive to the `/mnt` directory, to access its content
mount /dev/sda1 /media/pi/

# unmount
umount /media/pi/USB
```

# Install Software

## Docker

[Docker Docs Source](https://docs.docker.com/desktop/install/debian/)

```shell
# install
apt install docker.io docker-compose

# Start Docker Service
sudo systemctl enable --now docker

# Test Docker
sudo docker run --rm hello-world
```

### Troubleshoot

```shell
# Check status
systemctl status docker.service

# Reboot Docker Service
systemctl status docker.service
sudo systemctl stop docker
sudo reboot
# sudo systemctl enable docker
sudo systemctl start docker
```

## Picamera

- [source](https://picamera.readthedocs.io/en/release-1.13/install.html)

```shell
# Check if installed (if no errors, it's already installed).
python -c "import picamera"
python3 -c "import picamera"

# Install
sudo apt-get update
sudo apt-get install python-picamera python3-picamera

# update
sudo apt-get update
sudo apt-get upgrade

# remove installation
sudo apt-get remove python-picamera python3-picamera

# ---------------------------------------------------------------------------
# Alternate distro installation
# (probably simplest to install system wide using Python’s pip tool)
sudo pip install picamera

# upgrade installation
sudo pip install -U picamera

# remove installation
sudo pip uninstall picamera
# ---------------------------------------------------------------------------
```

# raspi-config

Raspberry Pi Configurations through CLI

## Boot Raspberry Pi to Desktop GUI

Open the Raspberry Pi configuration screen by running the following command:

```shell
sudo raspi-config
```

- Within the configurations screen, look for and select the option of **Enable Boot to Desktop/Scratch**.
- In the next screen, choose **Desktop Login as user 'Pi' at the graphical desktop**
- Reboot after configuration changes submitted.

## Disable Screen Blanking

[source](https://stackoverflow.com/a/72623494/14745606)

```shell
sudo raspi-config

# update configuration through interface
sudo reboot
```

# Tips

## Disable or Extend Sleep on Raspberry Pi

[source](https://stackoverflow.com/a/54239349/14745606)

Update `consoleblank` (a kernel parameter). In order to be permanently set, it needs to be defined on the kernel command line.

```shell
# view current console blanking settings
cat /sys/module/kernel/parameters/consoleblank
0
```
