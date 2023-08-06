**Table of Contents**
- [Terminology](#terminology)
  - [Bash](#bash)
  - [Comments](#comments)
  - [Shell](#shell)
  - [Shebang](#shebang)
- [Exit Status Codes](#exit-status-codes)
- [Make Script Executable](#make-script-executable)
- [Commands](#commands)
  - [read](#read)
- [Conditions](#conditions)
  - [Check Number of Input Args](#check-number-of-input-args)
  - [Check If Variable Empty](#check-if-variable-empty)


> [back to readme](../readme.md)

# Terminology
## Bash
*Bash (Bourne-again shell)* - a type of shell available for Linux that can run any system commands, utilities, processes, programs, or applications.

## Comments
Comments are prepended with the hash symbol (`#`) before each line. Comments are not read or executed by the interpreter.

## Shell
*shell* - an interface between the user and the operating system.


## Shebang
*shebang* - combination of a hash mark and an exclamation mark (`#!`) to communicate with the operating system which interpreter to use for the script.

Bash
```bash
#!/bin/bash
```

# Exit Status Codes
Every command executed by the shell script or user, has an exit status integer number.

| exit status       | value    |
|-------------------|--------- |
| 0                 | success  |
| non-zero (1-255)  | failure  |

> If a command is not found, the child process created to execute it returns a status of 127.
> If a command is found but is not executable, the return status is 126.


# Make Script Executable
Change the permissions of script file to execute. Give all perms for file owner and read/execute perms for group and other users
```shell
sudo chmod 755 {script_file}
```

# Commands
## read
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

# Conditions

## Check Number of Input Args
`$#` will return the number of arguments. Compare if value is equal to zero (`-eq 0`) to assert no arguments were supplied.
```shell
if [ $# -eq 0 ]; then
    echo "No arguments supplied"
fi
```

## Check If Variable Empty
Check if variable (or argument) is non-defined/empty. Use `-z {string}` to return True if the length of string is zero.
```shell
# True if argument ($1) has zero length
if [[ -z $1 ]]; then
  do something
fi
```

