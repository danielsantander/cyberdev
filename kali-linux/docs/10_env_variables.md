# Environment Variables

Environment variables: system-wide variables in key-value string pairs, they are inherited by any child shells or system processes.

> Shell variables - different from Environment variables in that they are only valid within shell they are created in

# Manage Environment Variables

## Viewing and Filtering Variables
View default environment variables on the system by entering the `env` command.
> syntax: `$ env`

```shell
$ env
HOME=/home/kali
LANG=en_US.UTF-8
LANGUAGE=
PWD=/home/kali
SHELL=/usr/bin/zsh
USER=kali
```

View all environment variables (local, shell) or any environment shell functions, use the `set` command.

> syntax: `$ set `
 
Pipe the `set` command with `more` to iterate through the variables line by line by pressing the return key (press `q` to quit).

```shell
$ set | more
HOME=/home/kali
LANG=en_US.UTF-8
LANGUAGE=
PWD=/home/kali
SHELL=/usr/bin/zsh
USER=kali
--More--
```


**Example** Filter through the list of environment variables to view the `HISTSIZE` value. (HISTSIZE value is the maximum number of commands the command history file will store.)
```shell
$ set | grep HISTSIZE
HISTSIZE=1000
```

## Change Variables

### Change variables for current session

> syntax for single value: `KEY=value`

> syntax for mutli values: `KEY=value0;value1;value3;` (multi values are common for setting the PATH variable)

**Example**: Change the `HISTSIZE` value so the system will not save past commands for the current session.
```shell
$ HISTSIZE=0
```

### Change variables permanently (export)

Use the `export` command to permanently export the new environment variable from current shell environment to the whole system.

> syntax: `$ export <variable_name>`

Note that if you are planning on chaning environment variables permanently, it might be a good idea to save the current variable values in a text document.
```shell
# make copy all environment variables
$ echo set > ~/ValuesOfAllVariables.txt

# make copy of just one
$ echo $HISTSIZE > ValueOfHISTSIZE.txt
```

**Example**: Use the `export` command to permanently change the `HISTSIZE` value.
```shell
$ echo $HISTSIZE
1000

$ HISTSIZE=0
$ export HISTSIZE
$ echo $HISTSIZE
0

# change back
$ HISTSIZE=1000
$ export HISTSIZE
$ echo $HISTSIZE
1000
```

**Example**: Change the shell prompt by updating the primary prompt environmnent variable `PS1`. The default prompt for kali is `username@hostname:current_directory`.

```shell

kali@kali: ~$ PS1='H@CK3R: $ '
                                                                  
H@CK3R: $ 

# export variable to make permanent across all sessions
H@CK3R: $ export PS1
```

**Example**: Update the `PATH` environment variable to include a new tool directory `/root/tools/MyNewTool`. To add a new variable to our PATH, we append the new path. `MyNewTool` can now be executed anywhere on the system.

> `PATH` controls where the shell will look for commands you enter (`pwd`, `cd`, `ls`, etc). The default PATH value is usually pointing to the `sbin` or `bin` directories (`/usr/local/sbin:/usr/local/bin`). Each directory value is separated by a colon (:).

```shell
# view current PATH
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:

# assign old PATH plus new tool directory to the new PATH
$ PATH=$PATH:/root/tools/MyNewTool

# tool directory is now appended to the PATH
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/tools/MyNewTool
```

> It's important to remember that you want to *append* to the `PATH`, *not* replace it's whole value.

**Example**: Create and remove a custom environment variable named ``
> Create a custom variable by assigning a value to a new variable. Remove the new variable by using the `unset` command.

```shell
# assign a new variable some value
$ NEWVARIABLE="Giving the new variable some value"

$ echo $NEWVARIABLE
> "Giving the new variable some value"

# use `unset` command to delete the new variable
$ unset NEWVARIABLE
$ echo NEWVARIABLE
> 
```

