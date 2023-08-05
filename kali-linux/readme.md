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
- [Packages and Services](#packages-and-services)
  - [Manage Services](#manage-services)
  - [Manage Software](#manage-software)
    - [Search for Packages](#search-for-packages)
    - [Installing Software](#installing-software)
    - [Updating Packages](#updating-packages)
    - [Upgrade Packages](#upgrade-packages)
    - [Removing Software](#removing-software)
    - [Remove Software and Configurations](#remove-software-and-configurations)
- [Applications](#applications)
  - [Apache Web Server (apache2)](#apache-web-server-apache2)
    - [Configure Web Server](#configure-web-server)
  - [Metasploit](#metasploit)
    - [PostgreSQL (postgres)](#postgresql-postgres)
    - [Start Metasploit](#start-metasploit)
    - [Setup PostgreSQL](#setup-postgresql)
    - [Connect to Database](#connect-to-database)
    - [sources](#sources)
  - [nmap](#nmap)
    - [Scan Type Options](#scan-type-options)
    - [Examples](#examples)
    - [Output Results to File](#output-results-to-file)
    - [sources](#sources-1)
  - [PostgreSQL](#postgresql)
    - [Create Database](#create-database)
    - [Create User](#create-user)
    - [Set Password](#set-password)
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
- [Commands](#commands)
  - [curl](#curl)
    - [GET Request](#get-request)
    - [POST Request](#post-request)
    - [PUT Request](#put-request)
    - [curl sources](#curl-sources)
  - [dig](#dig)
    - [dig options](#dig-options)
  - [find](#find)
    - [Find File Based on Content](#find-file-based-on-content)
    - [Search for Content with Regular Expressions](#search-for-content-with-regular-expressions)
- [Environment Variables](#environment-variables)
  - [Change variables](#change-variables)
  - [Update PATH](#update-path)

More Docs:
- [Documentation](docs/README.md)
  - [services](docs/15_services.md)
    - [Apache2](docs/15_services.md#apache-web-server)
    - [OpenSSH](docs/15_services.md#openssh)
  - [MySQL](docs/MySQL.md)
  <!-- - [Metasploit](docs/Metasploit.md)
    - [PostgreSQL](docs/Metasploit.md#postgresql-postgres) -->
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

> Tip: Combine command with `grep` to filter by process name `ps aux | grep {process_name}`

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

## find
```shell
# usage
find {LOCATION} {OPTIONS} {EXPRESSION}

# example -- find hidden files (files beginning with ".")
find . -type f -name '.*'

# example -- find log files by extension
find . -name ".log"

# example -- find files at the top of system owned by root user having a SUID permission bit set (-perm -4000)
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
find . -type f -exec grep "CONTENT_TO_SEARCH" '{}' \; -print
```
The curly braces (`{}`) are a placeholder for the `find` match results, and are enclosed with single quotes to avoid passing the `grep` command malformed filenames. The `-exec` command is terminated with an escaped semicolon (`\;`) to avoid interpretation  by the shell.

### Search for Content with Regular Expressions
```shell
# search current directory for a file containing text "TableOrderingFilter"
find . -type f -exec grep "\w*[T|t]able[O|o]rdering[F|f]ilter\w*" '{}' \; -print

# search for file containing "OrderingFilter" that does not begin with a period
find . -type f -exec grep "[^\.]*[O|o]rdering[F|f]ilter\w*" '{}' \; -print
```

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
