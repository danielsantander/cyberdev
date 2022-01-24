# File & Directory Permissions


## Different User Types (Groups)
Root user is all-powerfull and can do basically anything.

Grant users permissions to read, write, or execute files. For each file and directory, it is possible to specify permission status for the file's owner, groups of users, and other users.

Users are collected into groups that generally share similar functions. The goal is to put users with similar needs into a group that is granted relefant permissions, then each member of the group will inherit the group permissions.

> **Group inheritance**: `root user` is part of `root group` by default. Each new user will need to be added to a group in order to inherit the permissions of that group.

<hr>

## Grant Permissions
Three level of permissions:
1. `r` : permission to read (open and view a file)
2. `w` : permission to write (view and edit a file)
3. `x` : permission to execute (execute a file, but not necessarily view or edit)

When a file is created, the user who created that file is the file owner, and the owning group is the users' current group. 

### Granting Ownership to a User
Use the change owner (`chown`) command to move ownership of a file to a different user so they can control the permissions.

*Example*: grant user "john" ownership of "scriptfile"
```bash
# chown <user_to_give_ownership_to> <filename_location>
$ chown john /tmp/scriptfile
```

### Granting Ownership to a Group
Utilize the change group (`chgrp`) command to transfer ownership from one group to another.

Eample: change ownership of "newProgram" to the "blueTeam" group
```bash
# chgrp <group_name> <filename_location>
$ chgrp blueTeam newProgram
```

<hr> 

## Check Permisssions
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
7. Directory/file  name
```

<hr>

## Change Permissions
Use the change mode (`chmod`) command to change permissions (can only be done by root user or file owner>)

### Decimal Notation
Refer to permissions by using a single number to reporesent one 'rxw' set of permissions.

`rwx` values can be represented as binary numbers, where `111` in binary represents all permissions `rwx` granted. The `rwx` permission set can be represented as an octal number by converting it.

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
|        |       |     |

> To calculate the read & execute permission values (`r-x`), the binary representation would be `101`, and converted into octal would be `5`.

> To represent only read permissions (`r--`) the binary value would be `100` and the octal value would be `5`

To represent *all permissions* for the file owner, the group, and all users, we would use the same octal value for all three groups: `7 7 7`

Utilze the `chmod` command to change permissions for that directory/file for each of the three groups.

*Example*:
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

### Changing permissions with symbolic method (UGO)
Change permission with UGO (symbolic mothod). UGO stand for "user" (file owner), "group", and "others" (u, g o).
Using the 'rwx' notation, utilze the `chmod` command. 

> Note the `+-=` operator symbols are used to denote modifying permissions.
```
+ Adds permission(s)
- Removes permission(s)
= Sets permission(s)
```
After the operator symbol, list the permissions you would like to add/remove.

`$ chmod +rwx filename` to add read, write, and execute permissions for the file owner.

`$ chmod -rwx directoryname` to remove all permissions of the given directory for the file owner

`$ chmod +x filename` to give fileowner executable permissions on file.

`$ chmod -wx filename` to remove write and execute permissions of file for the file owner.


*Example*: grant the file owner executable permissions for `script.sh` file.
```bash
# note no executable permissions for file owner, only read and write permissions allowed:
$ ls -l
-rw-rw-r--1 kali kali 752 Sep  5 04:56 script.sh

# give executable permissions to file owner for script.sh.
$ chmod +x script.sh

$ ls -l
-rwxrwxr-x 1 kali kali 752 Sep  5 04:56 script.sh
```

#### Specify which user(s) to change permissions
Pass in an argument to the `chmod` command, just before the operator symbol to specify which user(s) to change permissions for.

**UGO Syntax:**
```
u symbolizes "User" (file owner)
g symbolizes "Group"
o symoblizes "Others"
```

```bash
$ chmod <ugo_value> <operator_value> <permissions_to_add_or_remove>
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

It is possible to change multiple permissions with one command. Just use a comma to delimit each permission change. Such as `chmod u-w, o+x script.sh`, which will both remove write permissions for the user (file owner) and grant others executable permissions for script.sh file.


### Grant Root Execute Permissions (for new tools)

Linux by default will set grant new directories and files permissions `777` and `666`, repectively. Meaning that these permissions do not include execute permissions. In order to be able to execute the new tool or program, give yourself root and execute permissions using the change mode command `chmod`.

*Example*: Give use execute permissions for a newly downloaded security tool.

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

## Default Permissions Using `Unmask`
Utilize the ummask (`umask`) method to change the default permissions allocated to directories/files created by each user.

### Unmask method
-  represents the permissions to *remove* from the base permissions on a file/directory.
-  three-digit decimal number corresponding to the three digits represengint a permission set.
-  the three-digit value used will be subtracted from the permissions number to give the new permissions status.

*Example*: If the default permissions for a new file is `666`, and the default permissions for a new directories are `777`, with `unmask` set to `022`, the new permissions for a new file will be `644` (022 subtracted from 666), and the new permissions for a new directory will be `755` (022 subtracted from 777).

> `umask` value is not universal to all users on the system. Each user can set a personal default `umask` value for the files and directories in their personal `.profile` file.

Change the `umask` value, edit the `/home/<username>/.profile` file.

```shell

# note the umask value for this user
$ umask
022

# edit the user profile file
# set umask to `007` - only user & members of the user's group will have permissions
$ vi /home/kali/.profile
umask 007
```

<hr>

## Special Permissions
Special permissions include:
- set user ID (SUID)
- set gorup ID (SGID)
- sticky bit

### Grant Temporary Root Permissions Using SUID

**SUID** bit value dictates if user can execute the file with the permissions of the owner. However, those permissions do not extend beyond the use of that file.

> use case: temporary grant owner's privileges to execute /etc/shadow file that holds the user's passwords, by setting the SUID bit on the program.

Set the SUID bit by entering a `4` before the regular permissions, so a file with a new permission of `644` (unmassked from `666`) is represented as `4644` when the `SUID` bit is set.

*Example*: Utilze the `chmod` command to change the SUID bit.
```bash
$ chmod 4644 filename
```

### Grant Root User's Group Permissions Using SGID



