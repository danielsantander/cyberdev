# Process Management
A *process* is a program being executed by one or more threads.

**Table of Contents**
- [Process Management](#process-management)
- [View Processes (ps)](#view-processes-ps)
  - [Filter By Name](#filter-by-name)
  - [List Process By Resources Used (top)](#list-process-by-resources-used-top)
- [Manage Processes](#manage-processes)
  - [Manipulate Priority](#manipulate-priority)
    - [Set priority when starting process (nice)](#set-priority-when-starting-process-nice)
    - [Change priority of running process (renice)](#change-priority-of-running-process-renice)
    - [Change priority of running process (top)](#change-priority-of-running-process-top)
- [Run Background Processes](#run-background-processes)
- [Foreground Processes](#foreground-processes)
- [Schedule Processes (at, cron, rc)](#schedule-processes-at-cron-rc)
  - [at command](#at-command)
  - [cron](#cron)
    - [Example Scheduling Tasks With Cron](#example-scheduling-tasks-with-cron)
  - [rc Scripts](#rc-scripts)
- [Killing System Processes (kill)](#killing-system-processes-kill)

<hr>

# View Processes (ps)
Each process will be assigned a unique process ID (PID) by the Linux kernel. The PID is assigned sequentially as they are created. View what processes are running on the system by using the `ps` command.

**Example**: Use the `ps` command without any arguments to view processes invoked by the currently logged in user.
```shell
$ ps        
 PID TTY          TIME CMD
 1088 pts/0    00:00:00 zsh
 1109 pts/0    00:00:00 ps                             
```

**Example**: Run the `ps` command with the `aux` option to view processes running on the system for all users.
```shell
$ ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.2  0.5  98628 10368 ?        Ss   Feb01   0:02 /sbin/init splash
...
...
kali        1249  0.0  0.1   9708  3372 pts/0    R+   00:11   0:00 ps aux
```

Output columns for command `ps aux`:
- `USER`: the user who invoked the process
- `PID`: process ID number
- `%CPU`: percent of CPU this processes is using
- `%MEM`: percent of memory this process is using
- `COMMAND`: command name that started this process

## Filter By Name
Use the `ps` command to list running processes and pipe it with the `grep` command to filter processes by name.
> `$ ps aux | grep <process_name>`

**Example**: Filter running processes to find the Metasploit process.
```shell
$ ps aux | grep msfconsole
kali        1626 11.4  8.1 732252 164936 pts/0   Sl+  00:35   0:04 ruby /usr/bin/msfconsole
kali        1654  0.0  0.1   6184  2272 pts/1    S+   00:36   0:00 grep --color=auto msfconsole
```
We can see that `msfconsole` is currently using 11.4% of resources (CPU usage) on the system.

## List Process By Resources Used (top)
The `top` produces a list of processes ordered by resources used, starting with the largest. The output will refresh dynamically, by default, every 10 seconds.

```shell
$ top
top - 01:23:40 up  1:28,  1 user,  load average: 0.12, 0.06, 0.02
Tasks: 143 total,   1 running, 142 sleeping,   0 stopped,   0 zombie
%Cpu(s):  1.9 us,  1.4 sy,  0.0 ni, 96.8 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   1982.8 total,    919.4 free,    406.8 used,    656.6 buff/cache
MiB Swap:    975.0 total,    975.0 free,      0.0 used.   1382.8 avail Mem 
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND       
    528 root      20   0  924804 104476  50836 S   3.0   5.1   0:11.62 Xorg          
    839 kali      20   0  152876   2756   2296 S   0.3   0.1   0:12.48 VBoxClient    
      1 root      20   0   98628  10368   7720 S   0.0   0.5   0:02.37 systemd       
```

<hr> 

# Manage Processes
Manage processes effectively to best utilize and optimize the system's resources.

## Manipulate Priority
Elevate the priority of a process with the `nice` command.

The "nice" value ranges from -20 to +19 with 0 being the default. Think of nice values as inverted in priority; the high nice value means a low priority, and a low nice value means a high priority. 

The owner of a process can only lower the priority, NOT increase the priority. However, a superuser or root user can arbitrarily set the nice value.

### Set priority when starting process (nice)

> syntax: `$ nice -n <niceness integer> <process to run>`

**Example**: Assuming we have a process `/usr/bin/myprocess`, start it with the `nice` command and increment the *nice value* by -10 (increasing the priority and allocating more resources to speed up it's  completion).
```shell
$ nice -n -10 /usr/bin/myprocess
```

### Change priority of running process (renice)
Only the root user can `renice` a system process to a negative value (giving it a higher priority).

> syntax: `$ renice <nice_value> <PID>`

The `renice` command takes two arguments:
1. an absolute value between -20 to 19 to set the priority
2. the process' PID number

**Example**: Give `myprocess` (with a PID value of 6789) a lower priority allocating more resource to other processes.
```shell
$ renice 20 6789
```

### Change priority of running process (top)
It is possible to renice a processes using the `top` command which outputs the currently running processes. With `top` running press the `R` key and then enter the `PID` of the process and the *nice value*.

<hr>

# Run Background Processes
Start a process and run in the background by appending an ampersand at the end of the command.

```shell
$ ./myscript &
```

# Foreground Processes
Move a process from the background to the foreground, use the `fg` command.

> syntax: `fg <PID>` where PID is the process' id number.

**Example**: Move the process with PID 6789 running in the background into the foreground. 
```shell
$ fg 6789
```

<hr>

# Schedule Processes (at, cron, rc)
Schedule commands to execute in the future with the `at` command or the `crond` command.
- Use the `at` daemon to schedule executions to run once at some point in time.
- Use the `cron` daemon to run recurring executions (daily, weekly, monthly, etc).
- Use `rc` scripts to run jobs/tasks at startup

## at command
`at` is a daemon--a background process--for scheduling an execution of a command(s) to run at a certain point in time. Enter the `at` command followed by the time to execute. You will then be brought into interactive mode and prompted to enter the command to execute the process.
> syntax: `at <time_to_execute>`

| Time Format          | Schedule                                |
|----------------------|-----------------------------------------|
| at 6:00am            | run at 6:00am on the current day        |
| at 6:00am April 1    | run at 6:00am on April 1st              |
| at noon              | run at noon on the current day          |
| at noon April 1      | run at noon on April 1st                |
| at 6:00am 02/20/2022 | run at 6:00PM on Feburary 20 20222      |
| at now + 20 minutes  | run in 20 minutes from the current time |
| at now + 12 hours    | run in 12 hours from the current time   |
| at now + 3 days      | run in 3 days from the current time     |
| at now + 2 weeks     | run in 2 weeks from the current time    |

**Example**: Schedule `myscript` to execute today at 8:00PM. 
```shell
$ at 8:00pm
at > /root/home/myscript
```

<hr>

## cron
Utilize the cron daemon (crond) and the cron table (cront) for scheduling recurring tasks to execute. The cron table is used to to schedule tasks/jobs, located at `/etc/contab`. The cron daemon checks the cron table for which commands to run at the specified times. Edit the cron table with the `cront` command followed by the `-e` argument (edit), you will then be prompted to edit the crontable: 

> syntax: `$ crontab -e`

Cron table input is represented as 7 fields: 

`<MINUTE> <HOUR> <DOM> <MON> <DOW> <user> <COMMAND>`

| FIELD              | Values |
|--------------------|--------|
| minute             | 0-59   |
| hour               | 0-23   |
| day of month (DOM) | 0-31   |
| month  (MON)       | 1-12   |
| day of week (DOW)  | 0-7    |

> use an asterisks (*) in place of the value to represent all values from that field.

```shell
$ crontab -e
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   comman
```

You can view or edit the crontab file directly:
```shell
$ cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#                                                           
```

### Example Scheduling Tasks With Cron

**Example**: Create a cron task to run a backup script (`/bin/backup.sh`) every Sunday morning at 1:00AM, specify that the user to run the script is "backup".
```shell
# run every Sunday of every month at 1AM:
00 1 * * 0 backup /bin/backup.sh
```

This cron task specifies to run `/bin/backup.sh` with `backup` user at the top of the hour (`00`) of the first hour (`1`), of any day of the month (`*`), of any month of the year (`*`), and on Sunday (`0`). Thus, the cron daemon will execute the backup script every Sunday morning at 1:00AM of every month.

**Example**: some more examples
```shell
# This will run only twice every month, on the 15th & 30th (regardless of what day), and at 1:00AM.
00 1 15,30 * * backup /bin/backup.sh

# This will run every weekday at 10:00PM
00 10 * * 1-5 backup /bin/backup.sh

# equivalent to the previous task
00 10 * * 1,2,3,4,5 backup /bin/backup.sh
```

## rc Scripts
Use the `update-rc.d` command to add or remove services to the `rc.d` script that will run at startup.

> syntax: `update-rc.d <script_or_service_name> <remove|defaults|disable|enable>

<hr>

# Killing System Processes (kill)
Use the `kill` command to stop a process.

> syntax: `$ kill -<signal> PID` where the signal flag is optional, and if not provided will use the default kill signal **SIGTERM** (15).

| signal  | number |                           about                              |
|---------|--------|--------------------------------------------------------------|
| SIGHUP  | 1      | Hangup signal (HUP): restarts process with same PID          |
| SIGKILL | 9      | Absolute kill signal, sends process' resources to /dev/null  |
| SIGTERM | 15     | Termination signal (TERM): default kill signal               |


**Example**: Kill a process with PID 6789.
```shell
$ kill -9 6789
```

**Example**: Restart the process using the Hangup (HUP) signal.
```shell
$ kill -1 6789
```

If the `PID` is unknown use the `killall` command which takes the name of the process instead of the process id number.

> syntax: `$ killall -<signal> <process_name>`

```shell
$ killall -9 myprocessname
```

