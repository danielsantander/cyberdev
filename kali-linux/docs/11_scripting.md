

**Table of Contents**
- [Bash Scripting](#bash-scripting)
- [HelloWorld Script](#helloworld-script)
  - [Make Script Executable](#make-script-executable)
- [Script Variables](#script-variables)
  - [Input Variables with read command](#input-variables-with-read-command)
- [NMAP Scripts](#nmap-scripts)


# Bash Scripting
*Shell* - an interface between the user and the operating system.

*Bash (Bourne-again shell)* - a type of shell available for Linux that can run any system commands, utilities, processes, programs, or applications.

*vi* and *vim* - text editors available for Linux.

*shebang* - combination of a hash mark and an exclamation mark (`#!`) to communicate with the operating system which interpreter to use for the script.


# HelloWorld Script
**Example** HelloWorld script which will return a message when executed. Start by declaring the shebang followed by `/bin/bash` to indicate the operating system should use the bash shell interpreter.

> note: Comments are prepended with the hash symbol (`#`) before each line. Comments are not read or executed by the interpreter.

HelloWorld script:
```
#! /bin/bash

# Hello world script

echo "Hello World!"
```

## Make Script Executable
Change the permissions in order to execute the script:
```shell
$ sudo chmod 755 HelloWorld
-rwxr-xr-x  1 kali  ...  HelloWorld
```

Execute the script from the current directory with `./<script_name>`
```shell
$ ./HelloWorld
```

# Script Variables
## Input Variables with read command
Use the `read` command to retrieve and save user input.
```shell
#! /bin/bash

# prompt user to input their name
echo 'What is your name?'

# save input into variable
read name

# output variable value
# echo 'Welcome' $name '!'
echo "Welcome ${name}!"
```

# NMAP Scripts
*nmap* - a network scanning tool used to discover hosts and services on a computer network by sending packets and analyzing the responses. Nmap provides a number of features for probing computer networks, including host discovery and service and operating system detection. [source](https://en.wikipedia.org/wiki/Nmap)

> nmap usage: `nmap <scan_type> <ip_address> <port>`

**Example** perform TCP scan on a given target and check if port 3306 port is open (MySQL default port).
```shell
$ nmap -sT 192.168.0.1 -p 3306
```

**Example** create bash script to prompt user for ip address & port number inputs
```shell
#! /bin/bash
echo "Enter starting IP address:"
read firstIP
echo "Enter last octet of the last IP address:"
read lastOctetIP
echo "Enter port number:"
read port

nmap -sT $firstIP-$lastOctetIP -p $port > /dev/null -oG ResultsMySQLScan
cat ResultsMySQLScan | grep open > ResultsOpenMySQLPorts
cat ResultsOpenMySQLPorts
```
