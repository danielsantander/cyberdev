**Table of Contents**
- [Scripts](#scripts)
  - [Exit Status Codes](#exit-status-codes)
- [Bash Scripting](#bash-scripting)
- [HelloWorld Script](#helloworld-script)
  - [Make Script Executable](#make-script-executable)
- [Script Variables](#script-variables)
  - [Input Variables with read command](#input-variables-with-read-command)
- [NMAP Script Example](#nmap-script-example)
- [Conditional Statements](#conditional-statements)


# Scripts

## Exit Status Codes
[src](https://www.cyberciti.biz/faq/linux-bash-exit-status-set-exit-statusin-bash/#:~:text=For%20the%20bash%20shell's%20purposes,the%20return%20status%20is%20126.)

- Every Linux or Unix command executed by the shell script or user, has an exit status.
- The exit status is an integer number.
- For the bash shell’s purposes, a command which exits with a zero (0) exit status has succeeded.
- A non-zero (1-255) exit status indicates failure.
- If a command is not found, the child process created to execute it returns a status of 127. If a command is found but is not executable, the return status is 126.
- All of the Bash builtins return exit status of zero if they succeed and a non-zero status on failure.

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

# NMAP Script Example
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

# Conditional Statements
