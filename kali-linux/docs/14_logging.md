**Table of Contents**
- [Logging](#logging)
- [log configuration](#log-configuration)
  - [log rules](#log-rules)
- [logrotate](#logrotate)
- [shred files](#shred-files)
- [disable logging](#disable-logging)


# Logging
Logging involves automatically storing events that occur when the operating system runs (including errors & security alerts).

Logs are stored based on a series of defined rules.

Monitoring log file use case: log files can leave 'footprints' of a users activities or even their identity. To secure a system, the user would need to know how to manage logging to determine if a system has been compromised, and by who.

> Each linux distribution uses their own logging service. For the sake of consistency with Kali Linux, we will be focusing on the `rsyslog` utility variation of syslogd. 

# log configuration
The `rsyslog` configuration file is usually located in the /etc/ directory at `/etc/rsyslog.conf`. 
You can modify the log configuration to update and set rules for what the system will automatically log.


## log rules
View the config file in a text editor and navigate down to the "Rules" section.
Here each line represents a logging rule for what logs are sent where.

Rule Format: `facility.priority     action` where:
- 'facility' references the program nam
- 'priority' the log level or what kind of messages to log
- 'action' references the filename and location at which to send the logs
> an asterisk (`*`) may be used as a wildcard to reference either all facilities and/or all priorities.

Logs are usually sent to `/var/log` with a descriptive filename displaying the facility/ program that generated them

```shell
$ vi /etc/rsyslog.conf
...
###############
#### RULES ####
###############

#
# First some standard log files.  Log by facility.
#
auth,authpriv.*                 /var/log/auth.log
*.*;auth,authpriv.none          -/var/log/syslog
#cron.*                         /var/log/cron.log
daemon.*                        -/var/log/daemon.log
kern.*                          -/var/log/kern.log
lpr.*                           -/var/log/lpr.log
mail.*                          -/var/log/mail.log
user.*                          -/var/log/user.log

#
# Logging for the mail system.  Split it up so that
# it is easy to write scripts to parse these files.
#
mail.info                       -/var/log/mail.info
mail.warn                       -/var/log/mail.warn
mail.err                        /var/log/mail.err

#
# Some "catch-all" log files.
#
*.=debug;\
        auth,authpriv.none;\
        mail.none               -/var/log/debug
*.=info;*.=notice;*.=warn;\
        auth,authpriv.none;\
        cron,daemon.none;\
        mail.none               -/var/log/messages

#
# Emergencies are sent to everybody logged in.
#
*.emerg                         :omusrmsg:*
```

> `*.emerg *` rule will log all events of type emergency (emerg) priority to all logged-on users.

# logrotate
Utilize log rotation to maintain log space, archiving log files by moving them to another location. The moved logged files will be cleaned out after a set period of time. This leaves space for more recent log files and having an archive or historical logs.

Information from thithe logrotate configuration file:
- The unit of time to rotate logs, default is set to `weekly`
- Interval at which to rotate logs, default (`rotate 4`) is set to rotating logs every 4 weeks
  - set `rotate 1` to set rotating logs to once a week, saving more storage space on the system
  - set `rotate 52` to set rotating logs to once a year
- Create a new log file after log rotation
  - uncomment `compressed` to enable compression of rotated logs

Log file archive naming:
After every rotation, log files and their archives are renamed. The most recent archived log file will have the same filename but with a `.1` append to it. The previous log file with 1 appended to it would be renamed with `.2`, and so on and so forth.
> this file archive naming convention implies that the last archived log file will be deleted.

*Example*: of archived log file for `/var/log/auth.log`. Notice the archived log file `/var/log/auth.log.4.gz`, after the next file log rotation (assuming default rsyslog.conf settings) this file will be deleted and replaced with log file `/var/log/auth.log.3.gz`.
```shell
$ ls -lh /var/log/auth.log* 
... /var/log/auth.log
... /var/log/auth.log.1
... /var/log/auth.log.2.gz
... /var/log/auth.log.3.gz
... /var/log/auth.log.4.gz
```

*Example*: With a text editor, open the logrotate config file located at `/etc/logrotate.conf`.
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

# shred files
Some users may want to remain stealthy and remove any logs of your activity. Utilize the `shred` command to delete the file and overwrite it several times. 

Usage: `shred -f -n <number_of_overwrites> <FILE>` where: 
- `-f` -> gives permission to shred files
- `-n` -> followed by the number of times to overwrite
  - > The more times a file is overwritten, the harder it is to recover. Overwriting larger files may be time-consuming.

*Example*: Use the `shred` command to delete and overwrite all auth log file 10 times. (Use the `*` to shred all auth logs including the rotated logs).
```shell
$ shred -f -n 10 /var/log/auth.log.*
```
Once successful, the contents of the auth log files should now be illegible.

# disable logging
Disable logging by using the `service` command to stop the rsyslog daemon.

Usage: `service <SERVICE_NAME> <start|stop|restart>

```shell
$ service rsyslog stop
```
Log files will now stop generating until the service is restarted.