
**Table of Contents**
- [Archiving Files](#archiving-files)
- [View Archived File Contents](#view-archived-file-contents)
- [Extract Archive File Contents](#extract-archive-file-contents)
- [Compressing Files](#compressing-files)
  - [gzip (GNU zip)](#gzip-gnu-zip)
  - [gunzip (GNU unzip)](#gunzip-gnu-unzip)
  - [bzip2](#bzip2)
  - [bunzip](#bunzip)
  - [compress](#compress)
  - [uncompress](#uncompress)
- [dd command](#dd-command)
<hr>

# Archiving Files
Creating a single file from many.
Utilize the `tar` command to compress files together and combine them into an archive.
> tar is short for tape archive

*Example*: Combine a pair of scripts into one single archive.
```shell
$ ls -lh
total 24K
-rwxr-xr-x 1 kali kali   55 Apr  6 20:33 HelloWorld
-rwxr-xr-x 1 kali kali 1.1K Apr  6 20:33 MySQLScan.sh

$ tar -cvf scriptArchive.tar HelloWorld MySQLScan.sh 
HelloWorld
MySQLScan.sh

$ ls -lh
-rwxr-xr-x 1 kali kali   55 Apr  6 20:33 HelloWorld
-rwxr-xr-x 1 kali kali 1.1K Apr  6 20:33 MySQLScan.sh
-rw-r--r-- 1 kali kali  10K Apr  6 20:41 scriptArchive.tar
```

The flags used:
- `c` option -> create
- `v` option -> verbose (optional)
- `f` option -> means to write to the following file (also works for reading files)

> note: Notice the file size of the archive (10K). The archive file is larger due to the 'tarring' overhead to create the archive file. This overhead becomes less and less significant with larger and larger files.

# View Archived File Contents
Display files from the tarbell without extracting them.

*Example*: Display the files within the archived file `scriptArchive.tar` without extracting the file using the `t` option.
```shell
$ tar -tvf scriptArchive.tar                        
-rwxr-xr-x kali/kali        55 2022-04-06 20:40 HelloWorld
-rwxr-xr-x kali/kali      1094 2022-04-06 20:33 MySQLScan.sh
```

# Extract Archive File Contents
Extract files from the tarball using the `tar` command with the `-x` switch.

*Example*: Extract the files from `scriptArchive.tar` into the current directory.
```shell
$ tar -xvf scriptArchive.tar
HelloWorld
MySQLScan.sh
```
> note: the `-v` switch will output which files are being extracted. Omit this switch to perform "silently" (without showing any output).

> note: if the extracted files already exist, `tar` will remove the existing files and replace them with the extracted files.


# Compressing Files

## gzip (GNU zip)
Utilize the `gzip` command to compress files. Uses extension `.tar.gz` or `.tgz`. 

*Example*: compress the `scriptArchive.tar` file.
```shell
$ ls -lh
-rw-r--r-- 1 kali kali  10K Apr  6 20:41 scriptArchive.tar

$ gzip scriptArchive.*  
-rw-r--r-- 1 kali kali  792 Apr  6 20:41 scriptArchive.tar.gz

```
> note: wildcard `*` used as file extension to denote that the command should apply to any file that begins with `scriptArchive` with any extension.

## gunzip (GNU unzip)
Utilize the `gunzip` command to decompress a `tar.gz` or `.tgz` file.

*Example*: decompress the `scriptArchive.tar.gz` file
```shell
$ gunzip scriptArchive.*

$ ls -lh
-rw-r--r-- 1 kali kali  10K Apr  6 23:27 scriptArchive.tar
```


## bzip2
Uses extension `.tar.bz2`, usually with better compression ratios than gzip.

*Example*: Use `bzip2` to compress the `scriptArchive.tar` file.
```shell
$ bzip2 scriptArchive.*  

$ ls -lh
-rw-r--r-- 1 kali kali  808 Apr  6 23:35 scriptArchive.tar.bz2
```

## bunzip
Utilize the `bunzip2` command to uncompress a compressed file.

*Example*: Use `bunzip2` to uncompress `scriptArchive.tar.bz2` file.
```shell
$ bunzip2 scriptArchive.tar.bz2

-rw-r--r-- 1 kali kali 10240 Apr  6 23:35 scriptArchive.tar
```

## compress
Uses extension `.tar.Z`

*Example*: Use the `compress` command to compress the `scriptArchive.tar` file.
```shell
$ compress scriptArchive.*

$ ls -lh
-rw-r--r-- 1 kali kali 1.1K Apr  6 23:35 scriptArchive.tar.Z
```

## uncompress
*Example*: Use the `uncompress` command to uncompress the `scriptArchive.tar.Z` file.
```shell
$ uncompress scriptArchive.*

ls -lh
-rw-r--r-- 1 kali kali  10K Apr  6 23:35 scriptArchive.tar
```

# dd command
Use the `dd` command to make a bit-by-bit physical copy of storage devices without logical structures such as a filesystem. This can be used to recover artifacts such as deleted files.

Usage: `dd if=inputfile of=outputfile`

*Example*: make a bit-to-bit copy of a flashdrive.
```shell
$ dd if=/dev/sdb of=/root/fashdrivecopy bs=4096 conv:noerror
```

Options:
- `bs` option -> determine the block size (bs) number of bytes read/written per block of data being copied [default = 512 bytes]
- `noerror` option -> continue to copy even if errors occur.

