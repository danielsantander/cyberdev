*Table of Contents*
- [Download Rasberry Pi OS](#download-rasberry-pi-os)
  - [View OS](#view-os)
  - [View Bit Size](#view-bit-size)
- [Update and Upgrade System](#update-and-upgrade-system)
- [Install Docker](#install-docker)
  - [Troubleshoot](#troubleshoot)
- [Install Picamera](#install-picamera)
- [raspi-config](#raspi-config)
  - [Boot Raspberry Pi to Desktop GUI](#boot-raspberry-pi-to-desktop-gui)

# Download Rasberry Pi OS
Download Raspberry Pi Operating Systems here: https://www.raspberrypi.com/software/operating-systems/

## View OS
```shell
cat /etc/os-release
```

## View Bit Size
```shell
uname -m
```
Output Expected:
- aarch64 (64 bit)
- armv7l (32 bit)

# Update and Upgrade System
```shell
sudo apt-get update && sudo apt-get upgrade
```

# Install Docker
[Docker Docs Source](https://docs.docker.com/desktop/install/debian/)

**Install**
```shell
apt install docker.io docker-compose
```

**Start Docker Service**
```shell
sudo systemctl enable --now docker
```

**Test Docker**
```shell
sudo docker run --rm hello-world
```

## Troubleshoot
Check status
```shell
systemctl status docker.service
```

Reboot Docker Service
```shell
systemctl status docker.service
sudo systemctl stop docker
sudo reboot
# sudo systemctl enable docker
sudo systemctl start docker
```

# Install Picamera
- [source](https://picamera.readthedocs.io/en/release-1.13/install.html)

Check (If no error, you’ve already got picamera installed)
```shell
python -c "import picamera"
python3 -c "import picamera"
```

Install
```shell
# install
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

Within the configurations screen, look for and select the option of **Enable Boot to Desktop/Scratch**.

In the next screen, choose **Desktop Login as user 'Pi' at the graphical desktop**

Reboot after configuration changes submitted.
