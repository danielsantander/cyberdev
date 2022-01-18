# Adding and Removing Software

Install software that did not come with the distribution or remove unwanted software.

Advanced Packaging Tool (APT) is the default software manager for debian-based Linux distributions. The primary command is `apt-get`


## Searching for package

Before downloading a software packate, check whether the package is available from the repository. 
```shell
$ apt-cache search <keyword>
```

## Adding Software
Use `apt-get install` command to install software.
```shell
$ apt-get install <package_name>

# Example:
$ apt-get install snort
```

## Removing Software
Use `apt-get remove` command to remove software.
```shell
$ apt-get remove <package_name>

# Example
$ apt-get remove snort
```

> The `remove` command does not remove the configuration file, allowing you to re-install the same package in the future without the need of reconfiguring settings.

## Remove Software AND Configurations
To remove the configuration file along with the software package, use the `apt-get purge` command.
```shell
$ apt-get purge <package_name>

# Example
$ apt-get purge snort
```

## Updating Software Packages
Use the `apt-get update` command to update the list of packages available for download form the repository. 

```shell
$ apt-get update
```

## Upgrading Software Packages
Use the `apt-get upgrade` command to actually upgrade the packages to the latest version.
```shell
$ apt-get upgrade
```

> `apt-get update` updates the list of available packages and their versions, but does not install or upgrade any packages. Whereas `apt-get upgrade` actually installs newer versions of the packages.


## Repository Source List File
The `source.list` file contains repositories the system will search for software. Update this file to define which repositories to download software.

To add a repository, add the name of the repository to the list and then save the file.

```shell
$ vi /etc/apt/sources.list
```

