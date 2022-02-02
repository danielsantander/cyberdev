# Process Management
A *process* is a program being executed by one or many threads.

Learn to manage processes:
1. View and find processes and how to discover which process are using the most resources
2. Manage processes by running them in the background, prioritizing them, and killing them if necessary.


**Table of Contents**
- [Process Management](#process-management)
- [View Processes (ps)](#view-processes-ps)
  - [Filter By Name](#filter-by-name)
  - [List Process By Resources Used (top)](#list-process-by-resources-used-top)
- [Manage Processes](#manage-processes)

<hr>

# View Processes (ps)
View what processes are running on the system. Each process will be assigned a unique process ID (PID) by the Linux kernel. The PID is assigned sequentially as they are crated. Utilize the `ps` command to view processes.

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
Utilize the `ps` command and pipe it with the `grep` command to filter running processes by name.
> `$ ps aux | grep <process_name>`

**Example**: Filter processes running to find the Metasploit process running.
```shell
$ ps aux | grep msfconsole
kali        1626 11.4  8.1 732252 164936 pts/0   Sl+  00:35   0:04 ruby /usr/bin/msfconsole
kali        1654  0.0  0.1   6184  2272 pts/1    S+   00:36   0:00 grep --color=auto msfconsole
```
We can see that `msfconsole` is currently using 11.4% of resources (CPU usage) on the system.

## List Process By Resources Used (top)
Utilize the `top` command to list processes by the highest used resources first. This command produces a list of processes ordered by resources used, starting with the largest.

The `top` command will refresh dynamically, by default, every 10 seconds.

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
