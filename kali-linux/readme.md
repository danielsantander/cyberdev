Table of Contents
- [Tips](#tips)
  - [Check Kali Linux Version](#check-kali-linux-version)
  - [Change Shell](#change-shell)
  - [Script Shebang](#script-shebang)
  - [Print Random Line From File](#print-random-line-from-file)
- [Permissions](#permissions)
  - [Change File Ownership](#change-file-ownership)
  - [Permission Levels](#permission-levels)
  - [Change Permissions](#change-permissions)
    - [UGO Symbolic Method](#ugo-symbolic-method)
  - [Check Permissions](#check-permissions)
  - [Configure Default Permissions](#configure-default-permissions)
- [Network](#network)
  - [Check Wireless Network Devices](#check-wireless-network-devices)
  - [Assign IP Address](#assign-ip-address)
    - [Troubleshoot](#troubleshoot)
  - [Change IP Address](#change-ip-address)
  - [Map IP Address To Host File](#map-ip-address-to-host-file)
  - [Change Network Mask and Broadcast](#change-network-mask-and-broadcast)
  - [Change MAC Address](#change-mac-address)
  - [Change DNS](#change-dns)
    - [Regenerate resolvconf](#regenerate-resolvconf)
    - [Install resolvconf service](#install-resolvconf-service)
- [Applications and Services](#applications-and-services)
  - [Manage Services](#manage-services)
  - [Manage Software](#manage-software)
    - [Search for Packages](#search-for-packages)
    - [Installing Software](#installing-software)
    - [Updating Packages](#updating-packages)
    - [Upgrade Packages](#upgrade-packages)
    - [Removing Software](#removing-software)
    - [Remove Software and Configurations](#remove-software-and-configurations)
- [Process Management](#process-management)
  - [ps](#ps)
  - [top](#top)
  - [nice](#nice)
  - [renice](#renice)
  - [Run Background Processes](#run-background-processes)
  - [Foreground Processes](#foreground-processes)
  - [Schedule Processes](#schedule-processes)
    - [at](#at)
    - [cron](#cron)
    - [rc](#rc)
  - [kill](#kill)
- [Commands](#commands)
  - [dig](#dig)
    - [dig options](#dig-options)

More Docs:
- [Documentation](docs/README.md)
  - [services](docs/15_services.md)
    - [Apache2](docs/15_services.md#apache-web-server)
    - [OpenSSH](docs/15_services.md#openssh)
  - [MySQL](docs/MySQL.md)
  - [Metasploit](docs/Metasploit.md)
    - [PostgreSQL](docs/Metasploit.md#postgresql-postgres)
- [Scripts](scripts/README.md)

---

# Tips
## Check Kali Linux Version
```bash
$ lsb_release -a
```

## Change Shell
```shell
# change to zsh shell
chsh -s /bin/zsh`
```

## Script Shebang
Script files will begin with the shebang: `#!/bin/bash`

## Print Random Line From File
```shell
# output "n" number of random lines from file
$ shuf -n 1 {filename}
```

# Permissions
## Change File Ownership
Use `chown` to change or grant ownership.
```shell
chown {user} {file}

# example
chown john /tmp/scriptfile
```

Use `chgrp` to grant a group ownership.
```shell
chgrp {group_name} {file}

# example
chgrp blueteam newProgram
```

## Permission Levels
Three level of permissions:
1. `r` : permission to read (open and view a file)
2. `w` : permission to write (view and edit a file)
3. `x` : permission to execute (execute a file, but not necessarily view or edit)

Represent a single set of permissions by using a numerical value.

Permissions can be represented as binary numbers, where `111` in binary represents all permissions granted whereas `000` represent none. The `rwx` permission set can be represented as an octal number by converting it form binary.

| rwx | Binary | Octal |
|-----|--------|-------|
| --- | 000    |   0   |
| --x | 001    |   1   |
| -w- | 010    |   2   |
| -wx | 011    |   3   |
| r-- | 100    |   4   |
| r-x | 101    |   5   |
| rw- | 110    |   6   |
| rwx | 111    |   7   |

## Change Permissions
Use `chmod` to change the directory and/or file permissions.

```shell
chmod {permission_value} {directory_or_file}

# give all permissions for file owner, group, and users
chmod 777 script.sh

# give all permissions for file owner,
# and only read/execute permissions for group and other users
chmod 755 script.sh
```

### UGO Symbolic Method
Change permissions with symbolic method (UGO). UGO stand for "user" (file owner), "group", and "others" (u, g o).

Operator symbols
```text
+ Adds permission(s)
- Removes permission(s)
= Sets permission(s)
```

```shell
chmod {UGO value} {operator value} {directory or file}

# example -- remove write perms from the user the file belongs to
chmod u-w script.sh

# example -- change multiple perms with one command using commas to delimit each
chmod u-w, o+x, script.sh

```

## Check Permissions
```shell
ls -l /home/
-rwxr-xr-x 1 root root 752 Sep  5 04:56 script.sh
```
The output should resemble:
```txt
d  rwxr-xr-x   1     root  root  752   Sep 5 04:56  script.sh
{1}   {2}     {3}    {4}         {5}    {6}         {7}

Where:
1. File type: first character of the line, 'd' for directory, '-' for file.
2. Permissions (rwxrwxrwx): in order of file ower, group, and all other users.
3. Number of links
4. Owner of file
5. File size (bytes)
6. Date created or last modified
7. Directory/file name
```

## Configure Default Permissions
Use `umask` to change default permissions for the user. Umask value is a three-digit decimal number subtracted from the permissions number to give the new permission status. Each user can set their default umask value (not universal) within their `.profile` file.

*Example*: If the default permissions for a new files are `666`, and the default permissions for new directories are `777`, with `unmask` set to `022`, the new permissions for files will be `644` (022 subtracted from 666), and the new permissions for directories will be `755` (022 subtracted from 777).

```shell
# view value
umask

# set value
vi /home/{user}/.profile

# example - set unmask to `007`
vi /home/root/.profile
umask 077
```

# Network
## Check Wireless Network Devices
`iwconfig` -- gather information such as the wireless adapter's IP address, MAC address, what mode it is in, and much more.

## Assign IP Address
Call DHCP server with `dhclient` to request IP address.
```shell
dhclient {interface}

# eth0 example
dhclient eth0

# wlan0 example
dhclient wlan0
```

### Troubleshoot
```shell
# ERROR:
dhclient wlan0
RTNETLINK answers: File exists

# SOLUTION #1: release the current lease & stop running DHCP client as previously recorded in the PID file
dhclient -r

# SOLUTION #2: remove all leases by removing file and getting new lease
sudo rm /var/lib/dhcp/dhclient.leases
sudo dhclient eth0
```

## Change IP Address
```shell
ifconfig {interface} {new_ip_address}

# Example
ifconfig eth0 192.168.180.115
```

## Map IP Address To Host File
Configure the `/etc/hosts` file for mapping to determine which IP address the browser directs a given domain.

> It's important to ensure you are using **TAB** between the IP address and the domain name, instead of spaces.

```shell
vi /etc/hosts
127.0.0.1       localhost
127.0.1.1       custom-domain-name
192.168.181.100	linux.org

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

## Change Network Mask and Broadcast
```shell
ifconfig eth0 192.168.180.115 netmask 255.255.0.0 broadcast 192.168.1.255
```

## Change MAC Address
Using `ifconfig` perform the following steps:
1. Use the `down` option to take down the interface (eth0 in this case)
2. Change the MAC Address
3. Bring up the interface with the `up` option

```shell
# eth0 Example:
ifconfig eth0 down
ifconfig eth0 hw ether 00:11:22:33:44:55
ifconfig eth0 up

# wlan0 Example
ifconfig wlan0 down
ifconfig wlan0 hw ether 00:11:22:33:44:55
ifconfig wlan0 up
```

## Change DNS
Update `/etc/resolv.conf` file:
1. Locate `resolv.conf` file
2. Update nameserver value

The machine will now go out to Google's DNS server rather than the initial local DNS server to resolve the domain names into IP addresses.

```shell
# resolv.conf file
cat /etc/resolv.conf
domain localdomain
search localdomain
nameserver 198.168.180.10

# update nameserver to Google's public DNS server 8.8.8.8
echo "nameserver 8.8.8.8" > /etc/resolv.conf
cat /etc/resolv.conf
nameserver 8.8.8.8
```

### Regenerate resolvconf
```shell
sudo resolvconf -u
```

### Install resolvconf service
```shell
# install resolvconf
sudo apt install resolvconf

# enable and then run service
systemctl enable resolvconf.service
systemctl start resolvconf.service

# check status
systemctl status resolvconf.service
```

# Applications and Services
## Manage Services
```shell
# Manage Services
service {service_name} {start|stop|restart}

# List Services
service --status-all | grep "+";
```

## Manage Software
Advanced Packaging Tool (apt) is the default software manager for debian-based Linux distributions. Usage: `apt-get`

### Search for Packages
```shell
# search for software packages before downloading
apt-cache search {keyword}
```

### Installing Software
```shell
apt-get install {package-name}
```

### Updating Packages
Update list of packages available for download from repository
```shell
apt-get update
```

### Upgrade Packages
Actually upgrade the packages to the latest version
```shell
apt-get upgrade
```

### Removing Software
```shell
apt-get remove {package-name}
```
> `remove` does not remove the configuration file. This allows future re-installation of the same package without then need of reconfiguring the settings.

### Remove Software and Configurations
```shell
apt-get purge {package-name}
```

# Process Management
## ps
View processes and their assigned process identification number (PID).
```shell
ps {options}

# example -- view processes running on the system for all users
ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
...
...
root        1249  0.0  0.1   9708  3372 pts/0    R+   00:11   0:00 ps aux
...
```

| OUTPUT   | DESCRIPTION                                |
|----------|--------------------------------------------|
| `User`   | the user who invoked the process
| `PID`    | process identification number
| `%CPU`   | percent of the CPU the process is using
| `%MEM`   | percent of memory the process is using
| `COMMAND`| command name that started this process

> Tip: Use with `grep` to filter by process name `ps aux | grep {process_name}`

## top
Use `top` command to produce a list of processes ordered by resources used, starting with the largest. The output will refresh dynamically every 10 seconds.

## nice
Start processes and manipulate their with the `nice` command. Elevate a process to allocate more resources speeding up it's completion.

The "nice" value ranges from -20 to +19 with 0 being the default. Think of nice values as inverted in priority; the high nice value means a low priority, and a low nice value means a high priority.

> The owner of a process can only lower the priority, NOT increase the priority. However, a superuser or root user can arbitrarily set the nice value.

```shell
nice -n {numerical_value} {process}

# example - start `myprocess` and increment the priority
nice -n -10 /usr/bin/myprocess
```

## renice
Change priority of a running process with `renice` command. Note that only the root user can update a system process to a negative value, giving it a higher priority.

```shell
renice {nice_value} {PID}

# example -- give a process a lower priority to allocate more resources to other processes
renice 20 6789
```

> Renice a process using the `top` command by entering the `R` key, the PID of the process, and then the new nice value.

## Run Background Processes
Append an ampersand `&` at the end of a command.

```shell
{command} &

# example
./myscript.sh &
```

## Foreground Processes
Move a process back to the foreground with `fg` command
```shell
fg {PID}

# example
fg 6789
```

## Schedule Processes
### at
A daemon to schedule executions to run once at some point of time.

```shell
at {time_to_execute}

# example -- schedule script to execute today at 8:00PM
at 8:00PM
at > /home/myscript.sh
```

| Time Format          | Schedule                                |
|----------------------|-----------------------------------------|
| at 6:00am            | run at 6:00am on the current day        |
| at 6:00am April 1    | run at 6:00am on April 1st              |
| at noon              | run at noon on the current day          |
| at noon April 1      | run at noon on April 1st                |
| at 6:00am 02/20/2022 | run at 6:00PM on February 20 20222      |
| at now + 20 minutes  | run in 20 minutes from the current time |
| at now + 12 hours    | run in 12 hours from the current time   |
| at now + 3 days      | run in 3 days from the current time     |
| at now + 2 weeks     | run in 2 weeks from the current time    |

### cron
Utilize the cron daemon (crond) and the cron table (cront) for scheduling recurring tasks to execute.

> `/etc/crontab` is the system wide crontab, whereas `crontab -e` is per user. Specify which user with `crontab -e -u <username>`

```shell
crontab -e

# m h  dom mon dow  command
*   *   *   *   *   echo 'foo'

# example - run a backup of all your user accounts at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
```

Cron table input is represented as 7 fields:
`<MINUTE> <HOUR> <DOM> <MON> <DOW> <user> <COMMAND>`

| FIELD              | Values |
|--------------------|--------|
| minute             | 0-59   |
| hour               | 0-23   |
| day of month (DOM) | 0-31   |
| month  (MON)       | 1-12   |
| day of week (DOW)  | 0-7    |
'

### rc
Use `update-rc.d` command to add or remove services to the `rc.d` script that will run at startup.

```shell
update-rc.d {script_or_service_name} {remove|defaults|disable|enable}

# example -- setup PostgreSQL to startup at system boot (ideal for avid users of Metasploit framework to store data). The following will add a line to rc.d script to start PostgreSQL on system boot.
update-rc.d postgresql defaults
```

## kill

Kill system processes.
```shell
kill -{signal_value} {PID}

# example -- kill a process
kill -9 6789

# example -- restart the process using HUP signal
kill -1 6789
```

> Tip: use `killall` command to provide the process name instead of the PID. `killall -{signal} {process_name}`

Signal Value Options (optional)
| signal  | num |                                                              |
|---------|-----|--------------------------------------------------------------|
| SIGHUP  | 1   | Hangup signal (HUP): restarts process with same PID          |
| SIGKILL | 9   | Absolute kill signal, sends process' resources to /dev/null  |
| SIGTERM | 15  | Termination signal (TERM): default kill signal               |

# Commands
## dig
Domain Information Groper (DIG) tool is used for performing DNS querying.
> By default `dig` uses the servers listed in `/etc/reolv.conf` file.

```shell
# usage
dig {domain}

# reverse DNS lookup usage:
dig -x {ip-address}

# specify name server w/ '@' symbol
dig {domain} @dns
dig linux.org @8.8.8.8  # ex query using Google's name server

# example
dig linux.org

; <<>> DiG 9.11.16-2-Debian <<>> linux.org
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 19330
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 8192
;; QUESTION SECTION:
;linux.org.                     IN      A

;; ANSWER SECTION:
linux.org.              300     IN      A       104.21.31.121
linux.org.              300     IN      A       172.67.176.128

;; Query time: 50 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Tue Sep 07 01:21:31 CDT 2021
;; MSG SIZE  rcvd: 70
```


### dig options
Specify options within home directory file `.digrc`
```
+nocmd +noall +answer
```

Some available options
```shell
# SHORT ANSWER TO QUERY
dig linux.org +short
172.67.176.128
104.21.31.121

# INCLUDE/EXCLUDE OUTPUT
# ------------------------
# exclude first two lines (version and global options)
dig {domain} +nocmd

# exclude header section (action performed and status)
dig {domain} +nocomments

# exclude OPT PSEUDOSECTION
dig {domain} +noedns

# exclude answer section
dig {domain} +noanswer

# exclude question section
dig {domain} +noquestion

# exclude stats (last section of the output)
dig {domain} +nostats


# include detailed answer -- turn off all results, then include answer
dig {domain} +noall +answer
```
