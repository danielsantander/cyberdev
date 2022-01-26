# File & Directory Permissions
Documentation for regulating file and directory permissions.

**Table of Contents**
- [File & Directory Permissions](#file--directory-permissions)
- [Users and Groups](#users-and-groups)
  - [Grant User File Ownership](#grant-user-file-ownership)
  - [Grant Group Ownership](#grant-group-ownership)
- [Permission Levels](#permission-levels)
- [Check Permisssions](#check-permisssions)
- [Change Permissions](#change-permissions)
  - [Decimal Notation](#decimal-notation)
  - [UGO Symbolic Method](#ugo-symbolic-method)
- [Grant User Execute Permissions](#grant-user-execute-permissions)
- [Config Default Permissions Using Masks](#config-default-permissions-using-masks)
- [Special Permissions](#special-permissions)
  - [Grant Temporary Root Permissions Using SUID](#grant-temporary-root-permissions-using-suid)
  - [Grant Root User's Group Permissions Using SGID](#grant-root-users-group-permissions-using-sgid)
    - [SGID applied to file](#sgid-applied-to-file)
    - [SGID applied to directory](#sgid-applied-to-directory)
- [Privilege Escalation](#privilege-escalation)
  - [Find Files Owned By Root](#find-files-owned-by-root)

<hr> 

# Users and Groups
Root user is all-powerfull and can do basically anything.

Grant users permissions to read, write, or execute files. For each file and directory, it is possible to specify permission status for the file's owner, groups of users, and other users.

Users are collected into groups that generally share similar functions. The goal is to put users with similar needs into a group that is granted relefant permissions, then each member of the group will inherit the group permissions.

> **Group inheritance**: `root user` is part of `root group` by default. Each new user will need to be added to a group in order to inherit the permissions of that group.

<hr>

## Grant User File Ownership
Use the change owner (`chown`) command to move ownership of a file to a different user so they can control the permissions.

*Example*: grant user "john" ownership of "scriptfile"
```bash
# chown <user_to_give_ownership_to> <filename_location>
$ chown john /tmp/scriptfile
```

## Grant Group Ownership
Utilize the change group (`chgrp`) command to transfer ownership from one group to another.

Eample: change ownership of "newProgram" to the "blueTeam" group
```bash
# chgrp <group_name> <filename_location>
$ chgrp blueTeam newProgram
```

<hr> 

# Permission Levels
Three level of permissions:
1. `r` : permission to read (open and view a file)
2. `w` : permission to write (view and edit a file)
3. `x` : permission to execute (execute a file, but not necessarily view or edit)

When a file is created, the user who created that file is the file owner, and the owning group is the users' current group. 

<hr>

# Check Permisssions
View permissions for a given file or directory by using the long listing (`ls`) command with the `-l` flag.

```bash
$ ls -l ~/code/
total 4
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

<hr>

# Change Permissions
Use the change mode (`chmod`) command to change permissions (can only be done by root or file owner)

## Decimal Notation
Represent a single set of permissions by using a numerical value.

`rwx` values can be represented as binary numbers, where `111` in binary represents all permissions granted and `000` represent none granted. The `rwx` permission set can be represented as an octal number by converting it form binary.

| Binary | Octal | rwx |
|--------|-------|-----|
| 000    |   0   | --- |
| 001    |   1   | --x |
| 010    |   2   | -w- |
| 011    |   3   | -wx |
| 100    |   4   | r-- |
| 101    |   5   | r-x |
| 110    |   6   | rw- |
| 111    |   7   | rwx |

To calculate the ocatal value of read & execute permissions `r-x`, calculate the binary representation and then convert into octal.
```
r-x -> convert into binary -> b'101 -> convert into octal -> 5
```

To represent only the read permissions `r--` the binary value would be `100` and the octal value would be `4`.

To represent *all permissions* for the file owner, the group, and all users, we would use the same octal value for all three groups: `7 7 7`

*Example*: Utilze the "change mode" command (`chmod`) to change the directory/file permissions for each of the three groups.
```bash
# before changing permissions
$ ls -l
-rwxr-xr-x 1 kali kali 752 Sep  5 04:56 script.sh

# allow file ower, groups, and users ALL permissions for this file
$ chmod 777 script.sh
$ ls -l
-rwxr-xr-x 1 kali kali 752 Sep  5 04:56 script.sh

# after changing permissions
$ ls -l
-rwxrwxrwx 1 kali kali 752 Sep  5 04:56 script.sh
```

## UGO Symbolic Method
Change permission with the symbolic method (UGO). UGO stand for "user" (file owner), "group", and "others" (u, g o).

Utlize the change mode command (`chmod`) along with an operator symbol and the `rwx` notation to modify permissions.

Operator symobls are used to modify permissions:
```
+ Adds permission(s)
- Removes permission(s)
= Sets permission(s)
```

After the operator symbol, list the permissions you would like to add/remove.

`$ chmod +rwx filename` to give file owner read, write, and execute permissions for the file.

`$ chmod -rwx directoryname` to remove all permissions of the given directory for the file owner

`$ chmod +x filename` to give file owner executable permissions for the file.

`$ chmod -wx filename` to remove file owner write and execute permissions for the file.


*Example*: Grant the file owner executable permissions for `script.sh` file.
```bash
# note no executable permissions for file owner, only read and write permissions allowed:
$ ls -l
-rw-rw-r--1 kali kali 752 Sep  5 04:56 script.sh

# give executable permissions to file owner for script.sh.
$ chmod +x script.sh

$ ls -l
-rwxrwxr-x 1 kali kali 752 Sep  5 04:56 script.sh
```

Pass in an argument to the `chmod` command, just before the operator symbol, to specify which user(s) to change permissions for.

**UGO Syntax:**
```bash
$ chmod <ugo_value> <operator_value> <permissions_to_add_or_remove>
# Where UGO values are either "u", "g", or "o".
# u symbolizes "User" (file owner)
# g symbolizes "Group"
# o symoblizes "Others"
```

*Example*: Remove the write permissions from the user that file `script.sh` belogs to.
```bash
# note file owner has write permissions for file:
$ ls -l
-rwxrwxr-x 1 kali kali 752 Sep  5 04:56 script.sh

# remove write permissions from the user the file belongs to
$ chmod u-w

# write permissions is now removed for user
$ ls -l
-r-xrwxr-x 1 kali kali 752 Sep  5 04:56 script.sh
```

Change multiple permissions with one command by using a comma to delimit each permission change. 
```bash
$ chmod u-w, o+x script.sh
```
Which will both remove write permissions for the user (file owner) and grant others executable permissions for script.sh file.


# Grant User Execute Permissions
Linux, by default, will set new directories and files permissions `777` and `666`, repectively. Therefore, these permissions do not include execute permissions. In order to be able to execute a new tool or program, give yourself root and execute permissions by utilizing the "change mode" command (`chmod`).

*Example*: Give user execute permissions for a newly downloaded security tool.
```bash
# new tool located in root directory (/) with no execute permissions for anyone
kali >ls -l
-rw-r--r-- 1 root root 1072 Sep  5 05:10 securitytool
 
# grant execute permission for user
kali >chmod 766 securitytool

# execute permissions granted
kali >ls -l
-rwxrw-rw- 1 root root 1072 Sep  5 05:10 securitytool
```

# Config Default Permissions Using Masks
Utilize the unmask (`umask`) method to change the default permissions allocated to directories/files created by each user.

Unmask:
-  represents the permissions to *remove* from the base permissions on a file/directory.
-  three-digit decimal number corresponding to the three digits represengint a permission set.
-  the three-digit value used will be subtracted from the permissions number to give the new permissions status.
-  value is not universal to all users on the system, each user can set a personal default `umask` value for the files and directories in their personal `.profile` file.
-  change the `umask` value, edit the `/home/<username>/.profile` file.

*Example*: If the default permissions for a new files are `666`, and the default permissions for new directories are `777`, with `unmask` set to `022`, the new permissions for files will be `644` (022 subtracted from 666), and the new permissions for directories will be `755` (022 subtracted from 777).
```bash
# note the umask value for this user
$ umask
022

# edit the user ".profile" file
# set umask to `007` - only user & members of the user's group will have permissions
$ vi /home/kali/.profile
umask 007
```

<hr>

# Special Permissions
Special permissions include:
- set user ID (SUID)
- set gorup ID (SGID)
- sticky bit

## Grant Temporary Root Permissions Using SUID

**SUID** bit value dictates if user can execute the file with the permissions of the owner. However, those permissions do not extend beyond the use of that file.

> use case: Set the SUID bit on the `/etc/shadow` (file that holds user's passwords) to temporary grant file owner privileges, allowing the user to execute the program, modifying their password.

Set the SUID bit by entering a `4` before the regular permissions. For example, a file with a new permission of `644` (unmassked from `666`) is represented as `4644` when the `SUID` bit is set.

*Example*: Utilze the `chmod` command to change the SUID bit.
```bash
$ chmod 4644 filename
```

## Grant Root User's Group Permissions Using SGID
### SGID applied to file
SGUID bit is represented by a `2` before the regular permissions.

SGUID grants temporary permissions of the file's group, rather than the file's owner.
The key feature here is that someone without execute permissions may be able to execute the file, **if** the owner belongs to the group that has permissions to execute that file.

### SGID applied to directory
When the SGID bit is applied to a directory, the ownership of new files goes to the directory creator's group, rather than the file creator's group.

> Use case: directory is shared by multiple users, and with SGID bit enabled all uses can execute files instead of just one.

# Privilege Escalation
Gaining root or sysadmin privileges.

**Example exploiting SUID/SGID bit**: A sysamind may set the SUID bit for a program to run the program with root privileges. An example would be to have a scrip that modifies credentials to have the SUID bit set. Utilize this knowledge to gain temporary root/sysadmin privileges and access other files such as `/etc/shadow/`.

## Find Files Owned By Root
*Example*: Find files owned by root user with SUID bit permission set.
```bash
# find at top of system (/) for files owned by user (root) and have a SUID permission bit set (-perm -4000)
$ find / -user root -perm -4000
...snip...
/usr/bin/sudo
/usr/bin/passwd
/usr/bin/su
/usr/bin/gpasswd
/usr/bin/chsh
/usr/bin/umount
/usr/bin/mount
...snip...

$ cd /user/bin
$ ls -l sudo
-rwsr-xr-x 1 root root 182600 Feb 27  2021 sudo
```

> Representing that the `SUID` bit is set, notice the `s` in place of the `x` for the first set of permissions (owner). Anyone who runs the sudo file has privileges of the root user.

Hackers may potentially exploit the SUID/SGID permissions to escalate privileges from a regular user to a sysadmin or root user.
