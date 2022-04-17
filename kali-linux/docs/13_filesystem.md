**Table of Contents**
- [The Linux Filesystem](#the-linux-filesystem)
  - [Device directory (dev)](#device-directory-dev)
  - [Partitions](#partitions)
- [List Block Devices (lsblk command)](#list-block-devices-lsblk-command)
- [Mounting Devices](#mounting-devices)
- [Unmounting Devices](#unmounting-devices)
- [Filesystem Monitoring (df command)](#filesystem-monitoring-df-command)
- [Filesystem Checks (fsck command)](#filesystem-checks-fsck-command)


# The Linux Filesystem
Linux manages storage devices with a file tree structure with root (`/`) being at the top.

**mounting**: attaching drives or disks to the filesystem, making them available to the operating system.

## Device directory (dev)
The device directory (located at `/dev/`) contains a file representing every device on the system. Each file's permission is denoted with either a `c` or `b`.
- character devices (`c`) ->  receive data character by character, such as keyboards or mice.
- block devices (`b`) -> communicate  in blocks of data (multiple bytes at a time), such as hard drives.

The devices listed as `sda1, sda2, sda3, sdb` represent the hard drive (or USB flash drive) and its partitions.

> Newer Serial ATA (SATA) interface drives and Small Computer System Interface (SCSI) hard drives are represented as `sda`

If more than one hard drives exist, Linux will increment the last letter of the name.
- `sda` -> First SATA hard drive
- `sdb` -> Second SATA hard drive
- `sdc` -> Third SATA hard drive

*Example*: Long list the device directory for any hard drives/USB flash drives, and their partitions:
```shell
$ ls -l /dev/sd*  
brw-rw---- 1 root disk 8, 0 Feb 12 14:06 sda
brw-rw---- 1 root disk 8, 1 Feb 12 14:06 sda1
brw-rw---- 1 root disk 8, 2 Feb 12 14:06 sda2
brw-rw---- 1 root disk 8, 5 Feb 12 14:06 sda5
```

## Partitions
Linux labels each partion of a storage drive with a number that comes after the drive designation. For example, the first partition of the first SATA drive will be designated as `sda1`, and the second partition of the first SATA drive will be `sda2`.

*Example*: Utilize the `fdisk` command to view the partitions on the Linux system (use the `-l`  switch to list all partitions on the drive).
```shell
$ fdisk -l                                                                    
Disk /dev/sda: 80 GiB, 85899345920 bytes, 167772160 sectors  
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xf0f6b9b0

Device     Boot     Start       End   Sectors  Size Id Type
/dev/sda1  *         2048 165771263 165769216   79G 83 Linux
/dev/sda2       165773310 167770111   1996802  975M  5 Extended
/dev/sda5       165773312 167770111   1996800  975M 82 Linux swap / Solaris
```

# List Block Devices (lsblk command)
*Example*: Utilize the `lsblk` (list block) command to list information about each block device within `/dev/`.
```shell
$ lsblk         
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0   80G  0 disk 
├─sda1   8:1    0   79G  0 part /
├─sda2   8:2    0    1K  0 part 
└─sda5   8:5    0  975M  0 part [SWAP]
sr0     11:0    1 1024M  0 rom
```
> MOUNTPOINT: position the drive was attached to the filesystem

# Mounting Devices
A storage device must be both physically and logically attached to the filesystem for the data to be available to the operating system. 

Mount points are locations in the directory tree where devices are attached to. Two main mount points in Linux are:
1. `/mnt` -> usually used to mount internal hard drives
2. `/media` -> usually used to mount external USB devices (flash drives) and external USB hard drives.

*Example*: Use the `mount` command to mount a new hard drive (`sdb1`) at the `/mnt` directory in order to access its content.
```shell
$ mount /dev/sdb1 /mnt
```
> The filesystems that are mounted on a system are kept in a file at `/etc/fstab/` (filesystem table) which is read by the system at every bootup.

# Unmounting Devices
"Eject" a device to keep from causing damage to the files stored on the device.

Usage: `unmount <file_entry_of_device>`

*Example*: Use the `unmount` command to unmount  the `sdb1` hard drive.
```shell
$ unmount /dev/sdb1
```
> note: Can not unmount a device that is busy, that is if the system is busy reading or writing data to the storage device.


# Filesystem Monitoring (df command)
Utilize the `df` command (disk free) to monitor the state of the filesystem.

The `df` command displays hard disks or mounted devices information such as disk space usage and availability.

Usage: `df <DRIVE>`
- DRIVE option is used to specify the drive to view information from, without specifying a drive it will return results for the first drive on the system. Specify a drive as such: `df sdb1`

*Example*: Use the disk free command to view information on the first drive on the system (in this case it's `sda1`)
```shell
$ df
Filesystem     1K-blocks     Used Available Use% Mounted on
...
/dev/sda1       81000912 11078484  65761816  15% /
...
```

# Filesystem Checks (fsck command)
Utilize the `fsck` command to check for any errors.

> You must unmount the drive before running a filesystem check else you will receive an error.

*Example*: Use the `fsck` filesystem check command to check for any errors on device `/dev/sdb1`. Remember to first unmount the device.
> note: use the `-p` option to have the command automatically fix any errors with the device.
```shell
$ unmount /dev/sdb1
$ fsck -p /dev/sdb1

fsck from util-linux 2.36.1
e2fsck 1.46.2
checking file system on /dev/sdb1
File system version   1.0
Sector size         512 bytes
Cluster size         32 kb
Volume size        7648 MB
Used space         1265 MB
Available space    6383 MB
Totally 20 directories and 111 files.
File system checking finished. No errors found
```