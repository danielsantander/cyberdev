*Table of Contents*
- [System Info](#system-info)
  - [View OS](#view-os)
  - [View Bit Size](#view-bit-size)
- [Update and Upgrade System](#update-and-upgrade-system)
- [Install Docker](#install-docker)
  - [Troubleshoot](#troubleshoot)

# System Info
Download Raspberry Pi Operating Systems here: https://www.raspberrypi.com/software/operating-systems/

## View OS
```shell
$ cat /etc/os-release

# returns the following:
PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
NAME="Raspbian GNU/Linux"
VERSION_ID="10"
VERSION="10 (buster)"
VERSION_CODENAME=buster
ID=raspbian
ID_LIKE=debian
HOME_URL="http://www.raspbian.org/"
SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
```

## View Bit Size
```shell
$ uname -m
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
```shell
systemctl status docker.service
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; disabled; vendor preset: enabled)
   Active: failed (Result: exit-code) since Fri 2022-08-26 02:36:09 CDT; 1min 3s ago
     Docs: https://docs.docker.com
 Main PID: 13459 (code=exited, status=1/FAILURE)

Aug 26 02:36:09 raspberrypi systemd[1]: docker.service: Service RestartSec=100ms expired, scheduling res
Aug 26 02:36:09 raspberrypi systemd[1]: docker.service: Scheduled restart job, restart counter is at 3.
Aug 26 02:36:09 raspberrypi systemd[1]: Stopped Docker Application Container Engine.
Aug 26 02:36:09 raspberrypi systemd[1]: docker.service: Start request repeated too quickly.
Aug 26 02:36:09 raspberrypi systemd[1]: docker.service: Failed with result 'exit-code'.
Aug 26 02:36:09 raspberrypi systemd[1]: Failed to start Docker Application Container Engine.
```

**Reboot Docker Service**
```shell
systemctl status docker.service
sudo systemctl stop docker
sudo reboot
# sudo systemctl enable docker
sudo systemctl start docker
```