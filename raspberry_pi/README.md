*Table of Contents*
- [Download Raspberry Pi OS](#download-raspberry-pi-os)
  - [View OS](#view-os)
  - [Check Linux Version](#check-linux-version)
  - [View Bit Size](#view-bit-size)
- [Update and Upgrade System](#update-and-upgrade-system)
- [Disable or Extend Sleep on Raspberry Pi](#disable-or-extend-sleep-on-raspberry-pi)
- [Install Docker](#install-docker)
  - [Troubleshoot](#troubleshoot)
- [Install Picamera](#install-picamera)
- [raspi-config](#raspi-config)
  - [Boot Raspberry Pi to Desktop GUI](#boot-raspberry-pi-to-desktop-gui)
  - [Disable Screen Blanking](#disable-screen-blanking)

---

# Download Raspberry Pi OS

Download Raspberry Pi Operating Systems here: https://www.raspberrypi.com/software/operating-systems/

## View OS

```shell
cat /etc/os-release
```

## Check Linux Version

```shell
lsb_release -a
```

## View Bit Size

```shell
uname -m
# Output Expected:
# - aarch64 (for 64 bit)
# - armv7l (for 32 bit)
```

# Update and Upgrade System

```shell
sudo apt-get update && sudo apt-get upgrade
```

# Disable or Extend Sleep on Raspberry Pi

[source](https://stackoverflow.com/a/54239349/14745606)

Update `consoleblank` (a kernel parameter). In order to be permanently set, it needs to be defined on the kernel command line.

```shell
# view current console blanking settings
cat /sys/module/kernel/parameters/consoleblank
0
```

# Install Docker

[Docker Docs Source](https://docs.docker.com/desktop/install/debian/)

```shell
# install
apt install docker.io docker-compose

# Start Docker Service
sudo systemctl enable --now docker

# Test Docker
sudo docker run --rm hello-world
```

## Troubleshoot

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

# Install Picamera

- [source](https://picamera.readthedocs.io/en/release-1.13/install.html)

```shell
# Check if installed (if no errors, it's already installed).
python -c "import picamera"
python3 -c "import picamera"
```

Install

```shell
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
