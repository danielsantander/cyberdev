EVERYTHING YOU NEED TO KNOW, AND MORE (EYNTKAM / EUN2K&M)
---
Table of Contents
- [Tips](#tips)
  - [Install](#install)
    - [Kali for Raspberry Pi 4](#kali-for-raspberry-pi-4)
    - [Install VS Code](#install-vs-code)
  - [Check Kali Linux Version](#check-kali-linux-version)
  - [View Bit Size](#view-bit-size)
  - [Determine revision of current firmware](#determine-revision-of-current-firmware)
  - [Update and Upgrade System](#update-and-upgrade-system)
  - [Generate SSH Keys](#generate-ssh-keys)
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
- [Packages and Services](#packages-and-services)
  - [Manage Services](#manage-services)
  - [Manage Software](#manage-software)
    - [Search for Packages](#search-for-packages)
    - [Installing Software](#installing-software)
    - [Updating Packages](#updating-packages)
    - [Upgrade Packages](#upgrade-packages)
    - [Removing Software](#removing-software)
    - [Remove Software and Configurations](#remove-software-and-configurations)
    - [Repository Source List File](#repository-source-list-file)
- [Applications](#applications)
  - [Apache Web Server (apache2)](#apache-web-server-apache2)
    - [Configure Web Server](#configure-web-server)
  - [Docker](#docker)
    - [Check Storage](#check-storage)
    - [System Prune](#system-prune)
    - [Delete](#delete)
    - [Reboot Docker Services](#reboot-docker-services)
  - [Metasploit](#metasploit)
    - [PostgreSQL (postgres)](#postgresql-postgres)
    - [Start Metasploit](#start-metasploit)
    - [Setup PostgreSQL](#setup-postgresql)
    - [Connect to Database](#connect-to-database)
    - [sources](#sources)
  - [MySql](#mysql)
    - [Commands](#commands)
    - [Connect to database](#connect-to-database-1)
    - [List Users](#list-users)
    - [Set Password](#set-password)
    - [SHOW Data](#show-data)
    - [SELECT Data](#select-data)
    - [Filter Data](#filter-data)
  - [nmap](#nmap)
    - [Scan Type Options](#scan-type-options)
    - [Examples](#examples)
    - [Output Results to File](#output-results-to-file)
    - [sources](#sources-1)
  - [OpenSSH](#openssh)
  - [PostgreSQL](#postgresql)
    - [Create Database](#create-database)
    - [Create User](#create-user)
    - [Set Password](#set-password-1)
    - [Associate User with Database](#associate-user-with-database)
    - [Drop Tables](#drop-tables)
    - [Truncate Table](#truncate-table)
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
- [Commands](#commands-1)
  - [bzip2 (compress)](#bzip2-compress)
  - [bunzip](#bunzip)
  - [compress](#compress)
  - [curl](#curl)
    - [GET Request](#get-request)
    - [POST Request](#post-request)
    - [PUT Request](#put-request)
    - [curl sources](#curl-sources)
  - [dd](#dd)
  - [df](#df)
  - [dig](#dig)
    - [dig options](#dig-options)
  - [find](#find)
    - [Find File Based on Content](#find-file-based-on-content)
    - [Search for Content with Regular Expressions](#search-for-content-with-regular-expressions)
  - [Filesystem Checks (fsck)](#filesystem-checks-fsck)
  - [gzip](#gzip)
    - [Compress gzip (GNU zip)](#compress-gzip-gnu-zip)
    - [Decompress gunzip (GNU unzip)](#decompress-gunzip-gnu-unzip)
  - [hostname](#hostname)
  - [netcat](#netcat)
  - [shred](#shred)
  - [tar](#tar)
    - [Compress](#compress-1)
    - [View Archived File Contents](#view-archived-file-contents)
    - [Extract Archive File Contents](#extract-archive-file-contents)
- [Environment Variables](#environment-variables)
  - [Change variables](#change-variables)
  - [Update PATH](#update-path)
- [Scripting](#scripting)
  - [Terms](#terms)
  - [Shebang](#shebang)
  - [Exit Status Codes](#exit-status-codes)
  - [Make Script Executable](#make-script-executable)
  - [Conditions](#conditions)
    - [Check Number of Input Args](#check-number-of-input-args)
    - [Check If Variable Is Empty](#check-if-variable-is-empty)
  - [Useful Commands](#useful-commands)
    - [read](#read)
- [Filesystem Management](#filesystem-management)
  - [Device Directory (/dev/)](#device-directory-dev)
  - [Partitions](#partitions)
  - [List Block Devices (lsblk)](#list-block-devices-lsblk)
  - [Mounting Devices (mount)](#mounting-devices-mount)
  - [Unmounting Devices (unmount)](#unmounting-devices-unmount)
  - [Filesystem Checks](#filesystem-checks)
- [Logging](#logging)
  - [Configuration](#configuration)
    - [Log Rules](#log-rules)
      - [Rule Format](#rule-format)
  - [Logrotate](#logrotate)
  - [Disable Logging](#disable-logging)
  - [Shred Files](#shred-files)

More Docs:
- [scripting](docs/scripting.md)
- [Documentation](docs/README.md)
  - [services](docs/15_services.md)
    - [Apache2](docs/15_services.md#apache-web-server)
    - [OpenSSH](docs/15_services.md#openssh)

---
# Tips

## Install

### Kali for Raspberry Pi 4

[src](https://www.kali.org/docs/arm/raspberry-pi-4/)

> **Prereq:** Recommendation is to use the 32-bit image on Raspberry Pi devices as that gets far more testing, and a lot of documentation out there expects you to be running RaspberryPi OS which is 32-bit.

### Install VS Code

Install VS Code from the Kali command line:

```shell
apt-get install code
```

## Check Kali Linux Version

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

## Determine revision of current firmware

```shell
uname -a
# Linux kermit 3.12.26+ #707 PREEMPT Sat Aug 30 17:39:19 BST 2014 armv6l GNU/Linux
#                         /
#                        /
#   firmware revision --+
```

## Update and Upgrade System

```shell
sudo apt-get update && sudo apt-get upgrade
```

## Generate SSH Keys

Generate a SSH key pair consisting of a public key and a private key.

```shell
# use -t option to specify key type
ssh-keygen -t rsa

# use -b option to specify length (in bit size)
ssh-keygen -b 2048 -t rsa

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
shuf -n 1 {filename}
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

> **Group inheritance**: `root user` is part of `root group` by default. Each new user will need to be added to a group in order to inherit the permissions of that group.

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
# usage
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
2. Permissions (rwxrwxrwx): in order of file owner, group, and all other users.
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
# usage:
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

Use `ifconfig` command to change the network mask (netmask) and broadcast address.

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

> The machine will now go out to Google's DNS server rather than the initial local DNS server to resolve the domain names into IP addresses.

### Regenerate resolvconf

```shell
sudo resolvconf -u
```

### Install resolvconf service

```shell
# install resolvconf
sudo apt-get install resolvconf

# enable and then run service
systemctl enable resolvconf.service
systemctl start resolvconf.service

# check status
systemctl status resolvconf.service
```

# Packages and Services

## Manage Services

A service is a program or application that runs in the background waiting to be used. Manage these services through the command line.

```shell
# Manage Services
service {service_name} {start|stop|restart}

# List Services
service --status-all | grep "+";

# start service
$ service {service_name} start

# stop service
$ service {service_name} stop

# restart service to capture any new configuration changes made
$ service {service_name} restart
```

## Manage Software

Advanced Packaging Tool (apt) is the default software manager for debian-based Linux distributions. Usage: `apt-get`

### Search for Packages

Before downloading a software package, check whether the package is available from the repository.

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

> `apt-get update` updates the list of available packages and their versions, but does not install or upgrade any packages. Whereas `apt-get upgrade` actually installs newer versions of the packages.

### Removing Software

```shell
apt-get remove {package-name}
```
> `remove` does not remove the configuration file. This allows future re-installation of the same package without then need of reconfiguring the settings.

### Remove Software and Configurations

```shell
apt-get purge {package-name}
```

### Repository Source List File

The `source.list` file contains repositories the system will search for software. Update this file to define which repositories to download software.

To add a repository, add the name of the repository to the list and then save the file.

```shell
vi /etc/apt/sources.list
```

# Applications

## Apache Web Server (apache2)

A free and open-source Web server software created by American software developer Robert McCool. Apache was released in 1995.

> Apache comes already installed on Kali Linux and many other Linux distros.

```shell
# install
apt-get install apache2

# start server -- once started, the default web page can be accessed at http://localhost/
sudo services apache2 start
```

### Configure Web Server

Apache's default index page is located at `/var/www/html/index.html`.

Update index page `/var/www/html/index.html`.

```html
<html>
  <body>
    <h1>Homepage</h1>
    <p>This is the new default web page.</p>
  </body>
</html>
```

> If the page is not updating, try restarting the Apache2 service with `sudo service apache2 restart`

## Docker

Check status

```shell
systemctl status docker.service
```

Start Container

```shell
docker start -i {container_id}
```

### Check Storage

Check Available Storage

```shell
docker system df
```

### System Prune

Use prune to do some clean up and remove unused data. (view more info: `docker system prune --help`)

```shell
docker system prune --all --force

# volumes are not pruned by default, must include `--volume`
docker system prune -a --volumes
```

Remove all unused local volumes.

```shell
docker volume prune
```

### Delete

Delete Untagged Images

```shell
docker rmi -f $(docker image ls -a | grep "<none>" | awk "{print \$3}")
```

### Reboot Docker Services

```shell
# check status
systemctl status docker.service

# stop docker
sudo systemctl stop docker

# reboot -- CAREFUL
sudo reboot

# sudo systemctl enable docker
sudo systemctl start docker
```

## Metasploit

Steps for exploiting a system:

1. Check if target system is vulnerable to an exploit
2. Select & configure an exploit
3. Select & configure a payload to utilize in the exploit
4. Select an encoding technique (remove 'bad characters' from the payload, known to cause the exploit to fail)
5. Execute the exploit

### PostgreSQL (postgres)

Install and start postgres before launching Metasploit.

```shell
# install postgres

apt-get install postgresql
# or
apt-get install postgresql-12

# start service
service postgres start

# check status
service postgresql --status
```

### Start Metasploit

With postgres running, launch Metasploit and enter the msfconsole.

```shell
# start metasploit, and enter console
msfconsole
```

### Setup PostgreSQL
Initialize DB

```shell
msf6 > sudo msfdb init
```

Reinitialize

```shell
msf6 > sudo msfdb reinit
```

Create user

```shell
# within msfconsole, switch user to obtain root privileges
msf6 > su postgres

# create metasploit framework user
postgres@kali:/home/kali$ createuser msf_user -P
Enter password for new role:
Enter it again:
postgres@kali:/home/kali$
```

Create Database

```shell
# create db with msf_user as owner
postgres@kali:/home/kali$ createdb --owner=msf_user my_hacker_db

# exit postgres
postgres@kali:/home/kali$ exit
```

### Connect to Database

Connect to database for Metasploit framework to store:

  - modules for fast results
  - results of system scans
  - exploits ran

```shell
# usage
msf6 > db_connect {USER}:{ENTER_PASSWORD_HERE}@{HOST}/{DATABASE_NAME}

# example (using localhost)
msf6 > db_connect msf_user:password123@127.0.0.1/my_hacker_db

# check status
msf6> db_status
[*] Connected to msf. Connection type: postgresql.

#disconnect database
msf6> db_disconnect
```

### sources

- [Metasploit Wiki](https://en.wikipedia.org/wiki/Metasploit_Project)

## MySql

```shell
# start service
service mysql start

# login
mysql -u {username} -p

# sudo command to login
sudo mysql -u {username} -p

# example -- root user's default password configuration is empty, press "ENTER" upon the password prompt
sudo mysql -u root -p
```

### Commands

|  operation  |   description                                       |
|-------------|-----------------------------------------------------|
| `SELECT`    | retrieve data                                       |
| `UNION`     | combine results of two or more `select` operations  |
| `INSERT`    | add/insert new data                                 |
| `UPDATE`    | modify/update existing data                         |
| `DELETE`    | remove/delete data                                  |

The two default admin databases (information_schema, performance_schema) and one non-admin database (mysql):

```sql
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
```

### Connect to database

```sql
USE {database_name}
```

### List Users

```sql
-- Retrieve user, host and password fields from `mysql` database and `user` table:
SELECT user, host, password FROM mysql.user;
```

### Set Password

```sql
-- set password for root user
UPDATE user SET password = PASSWORD("enter_password_here") where user = 'root';
```

### SHOW Data

Show databases.

```sql
-- view databases
SHOW DATABASES;

-- view databases
SHOW SCHEMAS;
```

Show tables.

```sql
SHOW TABLES FROM {database_name}

-- example show table of mysql
SHOW TABLES FROM mysql
```

Show columns.

```sql
-- display column field info of a table
DESCRIBE {database_name.table_name}

-- note: can also use 'DESC'
DESC {database_name.table_name}

-- note: can also do `SHOW COLUMNS`
SHOW COLUMNS FROM {table_name}

-- example
DESCRIBE mysql.user;
```

### SELECT Data

Retrieve data from a database table given the column name(s).

```sql
-- usage
SELECT <col1,col2,col3> FROM <table_name>;
```

### Filter Data

Use `LIKE` clause to filter the output given a pattern.

```sql
SHOW DATABASES LIKE {pattern};

-- example list databases with names that start with 'open'
SHOW DATABASES LIKE 'open%';
Empty set (0.000 sec)
```

> percent sign (%) is used to express matching zero, one, or multiple characters.

## nmap

Network scanning tool. Send packets analyze responses to discover hosts and services on a computer network.

```shell
# install
sudo apt-get install -y nmap

# usage
nmap {SCAN_TYPE} {IP/CIDR} {PORT}
```

> TIP: specify the `--packet-trace` option to report what is happening on the packet level.

### Scan Type Options

| option           |  description                                                  |
|------------------|---------------------------------------------------------------|
| -sL              | List Scan - simply list targets to scan                       |
| -sn              | Ping Scan - disable port scan                                 |
| -sP              | Ping Scan                                                     |
| -sS              | TCP SYN (Stealth) Scan -- requires raw-packet privileges      |
| -sT              | TCP Connect Scan                                              |
| -sV              | Probe open ports to determine service/version info            |
| -sO              | IP protocol scan                                              |
| -O               | Enable OS detection                                           |
| -n               | Never do DNS resolution                                       |
| -p {port ranges} | Only scan specified ports                                     |
|-v                | Increase verbosity level (use -vv or more for greater effect) |

### Examples

```shell
# Host Detection -- get live hosts
nmap -n -sP {IP/CIDR} | grep report | awk '{print $5}'

# TCP scan to check if port 3306 is open (MySQL default port)
nmap -sT {IP/CIDR} -p 3306

# OS Detection
nmap -O {IP/CIDR/HOST}

# OS Detection -- add -sV option to enable version detection, interrogating open ports.
nmap -sV -O -v 129.128.X.XX

```

### Output Results to File

```shell
nmap {SCAN_TYPE} {IP/CIDR} {PORT} > /dev/null -oG {OUTPUT_FILE}

# example
nmap -sT 192.168.x.x/16 -p 3306 > /dev/null -oG ResultsMySQLScan

# read 'open' results
cat ResultsMySQLScan | grep open > ResultsOpenMySQLPorts
cat ResultsOpenMySQLPorts
```

> TIP: `-oG` is deprecated, XML output format is far more powerful: `-oX` filespec (XML output)

### sources

- [nmap.org](https://nmap.org/)
  - [Port Scanning Techniques and Algorithms](https://nmap.org/book/scan-methods.html)
  - [Reference Guide](https://nmap.org/book/man.html)
- [nmap wiki](https://en.wikipedia.org/wiki/Nmap)

## OpenSSH
Secure shell (SSH) is used to securely connect to a remote system, which enables:

- creating a  user access list
- authentication with encrypted passwords
- communication encryption

Start service

```shell
service ssh start
```

SSH into the remote machine

```shell
ssh {user}@{address}
```

## PostgreSQL

```shell
# login
psql -U {USERNAME} {DATABASE}
```
Inside PostgreSQL
```sql
-- list user info
\du

-- deactivate pagination
\pset pager off

-- list database tables
\dt

-- list columns in table
\d {TABLE_NAME}
```

### Create Database

```sql
CREATE DATABASE {DB_NAME};
```

### Create User

```shell

# MacOS -- If postgres installed through Homebrew, create user by:
/usr/local/opt/postgres/bin/createuser -s {USERNAME}
```

### Set Password

```sql
\password {USERNAME}
```

### Associate User with Database

Create root user with admin privileges. Login to create a user that will have privileges to create and manage databases within the service.

```sql
CREATE ROLE newUser WITH LOGIN PASSWORD 'password';
ALTER ROLE newUser CREATEDB;

-- grant user access to a database
GRANT ALL PRIVILEGES {DATABASE_NAME} TO {USERNAME}
```

### Drop Tables

```sql
DROP TABLE {TABLE_NAME}
```

### Truncate Table

Truncate/remove data from table(s).

```sql
TRUNCATE {TABLE_NAME}, {SECOND_TABLE_NAME}
```

# Process Management

## ps

View processes and their assigned unique process identification number (PID).

```shell
# usage
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

> Tip: Combine command with `grep` to filter by process name `ps aux | grep {process_name}`

## top

Use `top` command to produce a list of processes ordered by resources used, starting with the largest. The output will refresh dynamically every 10 seconds.

## nice

Start processes and manipulate their priority with the `nice` command. Elevate a process to allocate more resources speeding up it's completion.

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

Start a process and run in the background by adding append an ampersand `&` at the end of a command.

```shell
# usage
{command} &

# example
./myscript.sh &
```

## Foreground Processes

Move a process back to the foreground with `fg` command

```shell
# usage
fg {PID}

# example
fg 6789
```

## Schedule Processes

### at

A daemon to schedule executions to run once at some point of time. Enter the `at` command followed by the time to execute, then an interactive shell prompt will be available to enter the command to execute.

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

Utilize the cron daemon (crond) and the cron table (cront) for scheduling recurring tasks to execute. The cron table is used to to schedule tasks/jobs, located at `/etc/contab`. The cron daemon checks the cron table for which commands to run at the specified times. Edit the cron table with the `cront` command followed by the `-e` argument (edit), you will then be prompted to edit the crontable.

> `/etc/crontab` is the system wide crontab, whereas `crontab -e` is per user. Specify which user with `crontab -e -u <username>`

```shell
crontab -e

# m h  dom mon dow  command
*   *   *   *   *   echo 'foo'

# example - run a backup of all your user accounts at 5 a.m every week with:
0 5 * * 1 tar -zcf /var/backups/home.tgz /home/

# This will run every weekday at 10:00PM
00 10 * * 1-5 backup /bin/backup.sh

# This will run every weekday at 10:00PM
00 10 * * 1-5 backup /bin/backup.sh
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

### rc

Use `update-rc.d` command to add or remove services to the `rc.d` script that will run at startup.

```shell
update-rc.d {script_or_service_name} {remove|defaults|disable|enable}

# example -- setup PostgreSQL to startup at system boot (ideal for avid users of Metasploit framework to store data).
# The following will add a line to rc.d script to start PostgreSQL on system boot.
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

> Tip: use `killall` command to provide the process name instead of the PID. `killall -{signal} {process_name}` -> example: `killall -9 myprocessname`

Signal Value Options (optional)
| signal  | num |                                                              |
|---------|-----|--------------------------------------------------------------|
| SIGHUP  | 1   | Hangup signal (HUP): restarts process with same PID          |
| SIGKILL | 9   | Absolute kill signal, sends process' resources to /dev/null  |
| SIGTERM | 15  | Termination signal (TERM): default kill signal               |

# Commands

## bzip2 (compress)

Use `bzip2` to compress files (usually with better compression ratios than gzip). Uses extension `.tar.bz2`

```shell
# example: compress the `scriptArchive.tar` file
bzip2 scriptArchive.*

ls -lh
-rw-r--r-- 1 kali kali  808 Apr  6 23:35 scriptArchive.tar.bz2
```

## bunzip

Uncompress a file with the `bunzip` command.

```shell
# example: uncompress `scriptArchive.tar.bz2` file.
bunzip2 scriptArchive.tar.bz2

-rw-r--r-- 1 kali kali 10240 Apr  6 23:35 scriptArchive.tar
```

## compress

`compress` command exports with file extension `.tar.Z`

```shell
# exports MyScript.tar.Z
compress MyScript.*
```

Uncompress

```shell
# exports MyScript.tar
uncompress MyScript.tar.Z
```

## curl

### GET Request

```shell
curl -X GET '{url}' --header "key:value ${ENVIRONMENT_VARIABLE}"
```

### POST Request

```shell
curl -X POST '{url}' -H "Content-Type: application/json" -d '{"key1":"value"}'
```

### PUT Request

```shell
curl -X PUT '{url}' -H "Content-Type: application/json" -d '{"key1":"value"}'
```

### curl sources

- [Site](https://curl.se/)
- [GitHub](https://github.com/curl/curl)
- [wiki](https://en.wikipedia.org/wiki/CURL)

## dd

Use `dd` to make a bit-by-bit physical copy of storage devices without logical structures such as a filesystem. This can be used to recover artifacts such as deleted files.

```shell
# usage
dd if=inputfile of=outputfile

# example: make bit-by-bit copy of flashdrive
dd if=/dev/sdb of=/root/flashdrivecopy bs=4096 conv:noerror
```

Where:
| arg        | description                                                                                 |
|------------|---------------------------------------------------------------------------------------------|
| `bs`       | block size: Num of bytes read/written per block of data being copied [default = 512 bytes]  |
| `noerror`  | Continue to copy even if errors occur.                                                      |

## df

Use Disk Free command `df` to monitor the state of the filesystem.

The df command displays hard disks or mounted devices information such as disk space usage and availability.

Usage where input `drive` is used to specify the drive to view information from. If no input, will default to the first drive on the system (i.e. `df sdb1`).

```shell
df {drive}

# example - specify the first drive of the system
df
Filesystem     1K-blocks     Used Available Use% Mounted on
...
/dev/sda1       81000912 11078484  65761816  15% /
...
```

## dig

Domain Information Groper (DIG) tool is used for performing DNS querying.
> By default `dig` uses the servers listed in `/etc/reolv.conf` file.

```shell
# check version
dig -v
DiG 9.10.6

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

```txt
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

## find

```shell
# usage
find {LOCATION} {OPTIONS} {EXPRESSION}

# example
find . -name "pattern" -print

# example -- find hidden files (files beginning with ".")
find . -type f -name '.*'

# example -- find log files by extension
find . -name ".log"

# example -- find files at the top of system (/) owned by root user having a SUID permission bit set (-perm -4000)
find / -user root -perm -4000
```

**Options**
| options                       | description                                                               |
|-------------------------------|---------------------------------------------------------------------------|
| -atime {NUMBER_OF_DAYS}       | file was accessed a given number of days ago                              |
| -mtime {NUMBER_OF_DAYS}       | file was modified a given number of days ago                              |
| -size  {FILE_SIZE_IN_BLOCKS}  | files in a given # of blocks (1 block = 512 bytes)                        |
| -type  {FILE_TYPE}            | specify file type (f=plain text, d=directory)                             |
| -exec  {UTILITY}              | True if the program named UTILITY returns a zero value as its exit status |
| -delete                       | Delete found files and/or directories. Always returns True                |

### Find File Based on Content
Execute `grep` command for every file that satisfies the conditions. Print matches to console.

```shell
find . -type f -exec grep "EXAMPLE_TEXT_TO_SEARCH" '{}' \; -print
```

The curly braces (`{}`) are a placeholder for the `find` match results, and are enclosed with single quotes to avoid passing the `grep` command malformed filenames. The `-exec` command is terminated with an escaped semicolon (`\;`) to avoid interpretation  by the shell.

### Search for Content with Regular Expressions

```shell
# search current directory for a file containing text "TableOrderingFilter"
find . -type f -exec grep "\w*[T|t]able[O|o]rdering[F|f]ilter\w*" '{}' \; -print

# search for file containing "OrderingFilter" that does not begin with a period
find . -type f -exec grep "[^\.]*[O|o]rdering[F|f]ilter\w*" '{}' \; -print
```

## Filesystem Checks (fsck)

Utilize the `fsck` command to check for any errors.

> You must unmount the drive before running a filesystem check else you will receive an error.

**Example:** Perform a filesystem check for any errors on device `/dev/sdb1/`

```shell

# first, unmount the device
unmount /dev/sdb1

# perform filesystem check
fsck -p /dev/sdb1
```

## gzip

### Compress gzip (GNU zip)

Compress files using the `gzip` command. Uses extensions `.tar.gz` or `.tgz`.

```shell
# example: compress the `scriptArchive.tar` file
ls -lh
-rw-r--r-- 1 kali kali  10K Apr  6 20:41 scriptArchive.tar

gzip scriptArchive.*
-rw-r--r-- 1 kali kali  792 Apr  6 20:41 scriptArchive.tar.gz
```

> Note: wildcard `*` used as file extension to denote that the command should apply to any file that begins with `scriptArchive` with any extension.

### Decompress gunzip (GNU unzip)

Use `gunzip` command to decompress a `tar.gz` or `.tgz` file.

```shell
# example: decompress the `scriptArchive.tar.gz` file
gunzip scriptArchive.*

ls -lh
-rw-r--r-- 1 kali kali  10K Apr  6 23:27 scriptArchive.tar
```

## hostname

Get IP Address and hostname information.

```shell
# usage
hostname -[option] [file]

# example -- use `-I` option to get all IP addresses.
hostname -I
```

## netcat

Allows users to read & write data over a network connection. Use it to execute remote commands, pass files back and forth, or even open a remote shell.

Usage, where host is either a numeric IP address or s symbolic hostname, and port is either a numeric port a service name

```shell
nc [<options>] <host> <port>
```

Command Options
| option    | type     | description        |
|-----------|----------|--------------------|
| -4        | protocol | Use IPv4 only      |
| -6        | protocol | Use IPv6 only      |
| -u, --udp | protocol | Use UDP connection |

## shred

Utilize the `shred` command to delete a file and overwrite it several times.

Usage: `shred -f -n {number_of_overwrites} {file}`

- `-f` -> gives permission to shred files
- `-n` -> followed by the number of times to overwrite
  - > The more times a file is overwritten, the harder it is to recover. Overwriting larger files may be time-consuming.

## tar

### Compress

Use `tar` command to compress files together and combine them into an archive (tape archive -> tar). The command will also compress files and directories recursively.

*Example*: Combine a pair of scripts into one single archive.

```shell
ls -lh
total 24K
-rwxr-xr-x 1 kali kali   55 Apr  6 20:33 HelloWorld
-rwxr-xr-x 1 kali kali 1.1K Apr  6 20:33 MySQLScan.sh

tar -cvf scriptArchive.tar HelloWorld MySQLScan.sh
HelloWorld
MySQLScan.sh

ls -lh
-rwxr-xr-x 1 kali kali   55 Apr  6 20:33 HelloWorld
-rwxr-xr-x 1 kali kali 1.1K Apr  6 20:33 MySQLScan.sh
-rw-r--r-- 1 kali kali  10K Apr  6 20:41 scriptArchive.tar

# example: compress a directory of stuff into a tar.
tar -cvf archive.tar stuff

# example: compress a directory of stuff into a gzip.
tar -czvf archive.tar.gz stuff
```

> Notice the file size of the archive (10K). The archive file is larger due to the 'tarring' overhead to create the archive file. This overhead becomes less and less significant with larger and larger files.

**tar options**
| option | description                                      |
|--------|--------------------------------------------------|
|    c   | create archive                                   |
|    f   | specify filename                                 |
|    t   | show files from tarbell without extracting them  |
|    v   | verbose                                          |
|    x   | extract files from the tarball                   |
|    z   | compress the archive with "gzip"                  |

### View Archived File Contents

Display files from the tarbell without extracting them.

```shell
# example: display files within `scriptArchive.tar` without extracting the file using the `t` option.
```shell
$ tar -tvf scriptArchive.tar
-rwxr-xr-x kali/kali        55 2022-04-06 20:40 HelloWorld
-rwxr-xr-x kali/kali      1094 2022-04-06 20:33 MySQLScan.sh
```

### Extract Archive File Contents

Extract files from the tarball using the `tar` command.

```shell
# example: extract the files from `scriptArchive.tar` into the current directory.
tar -xvf scriptArchive.tar
HelloWorld
MySQLScan.sh
```

> Notes:
>
> - The `-v` switch will output which files are being extracted. Omit this switch to perform "silently" (without showing any output).
> - If the extracted files already exist, `tar` will remove the existing files and replace them with the extracted files.

# Environment Variables

Key-value string pairs that are inherited by any child shells or system processes.
> Shell variables: different from Environment variables in that they are only valid within shell they are created in.

```shell
# view default environment variables on the system
env

# view shell-local variables (including shell functions) -- pipe with 'more' to iterate
set | more

# example -- use `grep` to filter environment variables
set | grep HISTSIZE
HISTSIZE=500

# example -- change variable `HISTSIZE` so the system will not save past commands for the current session
HISTSIZE=0
```

## Change variables

Change variables for current session

```shell
# single value usage:
KEY=value

# multi value usage (common for setting PATH)
KEY=value0;value1;value3;`

# example -- Change shell prompt by updating `PS1`
# The default prompt for kali is `username@hostname:current_directory`
kali@kali: ~$ PS1='H@CK3R: $ '
```

> export variable to make permanent across all sessions: `export PS1`

Change variables system wide with `export` command

```shell
export KEY=value

# example -- Change shell prompt by updating `PS1`
# The default prompt for kali is `username@hostname:current_directory`
PS1='H@CK3R: $ '
# export variable to make permanent across all sessions
export PS1

# example - update HISTSIZE system wide
export HISTSIZE=100
echo $HISTSIZE
100
```

May be a good idea to save the current variable values in a text document before changing ENV variables system wide.

```shell
# make copy all environment variables
$ echo set > ~/ValuesOfAllVariables.txt

# make copy of just one
$ echo $ENV_NAME > ValueOf_ENV_NAME.txt
```

use `unset` command to delete the new variable

```shell
$ unset NEWVARIABLE
$ echo NEWVARIABLE
```

## Update PATH

Update `PATH` environment variable to include a new tool directory named `/root/tools/MyNewTool` to allow `MyNewTool` to be executed anywhere on the system.

> It's important to remember that you want to *append* to the `PATH`, *not* replace it's whole value.

```shell
# view PATH
echo $PATH

# update PATH
PATH=$PATH:/root/tools/MyNewTool
```

# Scripting

## Terms

*Bash (Bourne-again shell)* - A type of shell available for Linux that can run any system commands, utilities, processes, programs, or applications.

*shell* - An interface between the user and the operating system.

*mounting* - Attaching drives or disks to the filesystem, making them available to the operating system.

## Shebang

*shebang* - combination of a hash mark and an exclamation mark (`#!`) to communicate with the operating system which interpreter to use for the script.

Bash

```bash
#!/bin/bash
```

Python

```python
#!/usr/bin/env python
#!/usr/bin/python3
```

## Exit Status Codes

Every command executed by the shell script or user, has an exit status integer number.

| exit status       | value    |
|-------------------|--------- |
| 0                 | success  |
| non-zero (1-255)  | failure  |

> If a command is not found, the child process created to execute it returns a status of 127.
> If a command is found but is not executable, the return status is 126.

## Make Script Executable

Change the permissions of script file to execute. Give all perms for file owner and read/execute perms for group and other users.

```shell
sudo chmod 755 {SCRIPT}
```

## Conditions

### Check Number of Input Args

Use `$#` to return the number of arguments.

Compare if number of args is equal to zero (`-eq 0`) to assert no arguments were supplied.

```shell
if [ $# -eq 0 ]; then
    echo "No arguments supplied"
fi
```

### Check If Variable Is Empty

Check if variable is non-defined/empty. Use `-z {string}` to return True if the length of string is zero.

```shell
# True if argument ($1) has zero length
if [[ -z $1 ]]; then
  do something
fi
```

## Useful Commands

### read

Use the `read` command to retrieve and save user input.

```shell
#! /bin/bash
echo 'What is your name?'

# save input into variable
read name

echo "Welcome ${name}!"
```

# Filesystem Management

## Device Directory (/dev/)

The device directory (located at `/dev/`) contains a file representing every device on the system. Each file's permission is denoted with either a `c` or `b`.

- character devices (`c`): receive data character by character, such as keyboards or mice.
- block devices (`b`): communicate  in blocks of data (multiple bytes at a time), such as hard drives.

The devices listed as `sda1, sda2, sda3, sdb` represent the hard drive (or USB flash drive) and its partitions.
> Newer Serial ATA (SATA) interface drives and Small Computer System Interface (SCSI) hard drives are represented as `sda`. If more than one hard drives exist, Linux will increment the last letter of the name.
>
> - `sda` -> First SATA hard drive
> - `sdb` -> Second SATA hard drive
> - `sdc` -> Third SATA hard drive

```shell
# long list the device directory for any hard drives/USB flash drives, and their partitions
ls -l /dev/sd*
```

## Partitions

Partitions of a storage device are labeled with a number after the drive designation name. For example, the first partition of the first SATA drive will be designated as sda1, and the second partition of the first SATA drive will be sda2.

Use `fdisk` command to view the partitions on the Linux system (use w/ `-l` to list all partitions on the drive).

```shell
fdisk -l
```

## List Block Devices (lsblk)

Use `lsblk` (list block) command to list information about each block device within `/dev/`.

```shell
lsblk

# will output table with following header
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
...
```

> The column `MOUNTPOINT` is the position/location the drive was attached to the filesystem.

## Mounting Devices (mount)

A storage device must be both physically and logically attached to the filesystem for the data to be available to the operating system.

Mount pionts are locations in the directory tree where the devices area attached to. Two main mount opints in Linux are:

1. `/mnt`: Usually used to mount internal hard drives.
2. `/media`: Usually used to mount external USB devices (flash drives) and external USB hard drives.

> The filesystems that are mounted on a system are kept in a file at `/etc/fstab/` (filesystem table) which is read by the system at every bootup.

Example of mouning hard drive.

```shell
# mount a sbd1 hard drive to the /mnt directory, to access its content
mount /dev/sdb1 /mnt
```

## Unmounting Devices (unmount)

"Eject" a device to keep from causing damage to the files stored on the device.
> Can not unmount a device that is busy, that is if the system is busy reading or writing data to the storage device.

```shell
# usage:
unmount {file_entry_of_device}
```

## Filesystem Checks

Utilize the [Disk Free `df` command](#df) to monitor the state of the filesystem.

Perform filesystem checks on devices with the [Filesystem check `fsck` command](#filesystem-checks-fsck).

# Logging

Logging involves automatically storing events that occur when the operating system runs (including errors & security alerts).

Logs are stored based on a series of defined rules.

> Log files can leave 'footprints' of a users activities or even their identity. To secure a system, the user would need to know how to manage logging to determine if a system has been compromised, and by who.

> Each linux distribution uses their own logging service. For the sake of consistency with Kali Linux, we will be focusing on the `rsyslog` utility variation of syslogd.

## Configuration

The `rsyslog` configuration file is usually located at `/etc/rsyslog.conf`

You can modify the log configuration to update and set rules for what the system will automatically log.

### Log Rules

With a text editor navigate down to the "Rules" section of the rsyslog.conf file. Each line represents a logging rule for what logs are sent where.

#### Rule Format

Rule Format: `facility.priority     action` where:

- 'facility' references the program name
- 'priority' the log level or what kind of messages to log
- 'action' references the filename and location at which to send the logs

> an asterisk (`*`) may be used as a wildcard to reference either all facilities and/or all priorities.

## Logrotate

The logrotate config file is usually located at `/etc/logrotate.conf`.

Utilize log rotation to maintain log space, archiving log files by moving them to another location. The moved logged files will be cleaned out after a set period of time. This leaves space for more recent log files and having an archive or historical logs.

Logroate Configuration file information:

- The unit of time to rotate logs, default is set to `weekly`
- Interval at which to rotate logs, default (`rotate 4`) is set to rotating logs every 4 weeks
  - set `rotate 1` to set rotating logs to once a week, saving more storage space on the system
  - set `rotate 52` to set rotating logs to once a year
- Create a new log file after log rotation
  - uncomment `compressed` to enable compression of rotated logs

**Example:** With a text editor, open the logrotate config file located at `/etc/logrotate.conf`.

```shell
$ vi /etc/logrotate.conf
# see "man logrotate" for details

# global options do not affect preceding include directives

# rotate log files weekly
weekly

# keep 4 weeks worth of backlogs
rotate 4

# create new (empty) log files after rotating old ones
create

# use date as a suffix of the rotated file
#dateext

# uncomment this if you want your log files compressed
#compress

# packages drop log rotation information into this directory
include /etc/logrotate.d

# system-specific logs may also be configured here.
```

## Disable Logging

Disable logging by using the `service` command to stop the rsyslog daemon.

```shell
service rsyslog stop
```

Log files will now stop generating until the service is restarted.

## Shred Files

Use the [`shred` command](#shred) to delete a file and overwrite it several times.

**Example:** Use the `shred` command to delete and overwrite all auth log file 10 times. (Use the `*` to shred all auth logs including the rotated logs).

```shell
shred -f -n 10 /var/log/auth.log.*
```

Once successful, the contents of the auth log files should now be illegible.
