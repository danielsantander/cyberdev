- [Metasploit](#metasploit)
  - [PostgreSQL (Postgres)](#postgresql-postgres)
    - [Check postgresql status](#check-postgresql-status)
    - [Install PostgreSQL](#install-postgresql)
    - [Start Postgres Service](#start-postgres-service)
- [Start Metasploit](#start-metasploit)
  - [Setup PostgreSQL](#setup-postgresql)
    - [Log Into Postgres as root from Metasploit Framework](#log-into-postgres-as-root-from-metasploit-framework)
    - [Create user](#create-user)
    - [Create Database Set Permissions](#create-database-set-permissions)
- [Terms](#terms)
- [Sources:](#sources)


# Metasploit
Open source software tool for developing and executing exploit code against a targeted machine.

Steps for exploiting a system:
1. Check whether target system is vulnerable to an exploit
2. Choose and configure an exploit
3. Choose and configure a payload to utilize in the exploit
4. Choose an encoding technique (remove 'bad characters' from the payload, known to cause the exploit to fail)
5. Execute the exploit

## PostgreSQL (Postgres)
Postgres is an open source relational database known for it's easy scalability. It is the default database for most widely used penetration testing frameworks (including Metasploit). Metasploit utilizes Postgres to store its modules, exploits, and scan results.

### Check postgresql status
```
service postgresql --status                             130 ⨯
Usage: /etc/init.d/postgresql {start|stop|restart|reload|force-reload|status} [version ..]
```

### Install PostgreSQL
`apt-get postgresql install`

### Start Postgres Service
`service postgresql start`
> may need to authenticate with sudo user credentials


# Start Metasploit
With Postgres running, start Metasploit with the `msfconsole` command. Upon successful startup, you will enter the `msf` command prompt.

```shell
$ msfconsole
msf > 
```

## Setup PostgreSQL
Setup the PostgreSQL database to store data from the Metasploit framework.
```shell
msf6 > sudo msfdb init
[*] exec: msfdb init

[i] Database already started
[+] Creating database user 'msf'
[+] Creating databases 'msf'
┏━(Message from Kali developers)
┃
┃ We have kept /usr/bin/python pointing to Python 2 for backwards
┃ compatibility. Learn how to change this and avoid this message:
┃ ⇒ https://www.kali.org/docs/general-use/python3-transition/
┃
┗━(Run: “touch ~/.hushlogin” to hide this message)
[+] Creating databases 'msf_test'
┏━(Message from Kali developers)
┃
┃ We have kept /usr/bin/python pointing to Python 2 for backwards
┃ compatibility. Learn how to change this and avoid this message:
┃ ⇒ https://www.kali.org/docs/general-use/python3-transition/
┃
┗━(Run: “touch ~/.hushlogin” to hide this message)
[+] Creating configuration file '/usr/share/metasploit-framework/config/database.yml'
[+] Creating initial database schema
msf6 >
```

Reinitialize with command:
```
msf6 > sudo msfdb reinit
[*] exec: sudo msfdb reinit
```


### Log Into Postgres as root from Metasploit Framework
Use `su` to switch user in order to obtain root privileges.
```ssh
msf6 > su postgres
[*] exec: su postgres

postgres@kali:/home/kali$ 
```
> prompt changes represent application, hostname, and then user.

### Create user
```shell
postgres@kali:/home/kali$ createuser msf_user -P
Enter password for new role: 
Enter it again: 
postgres@kali:/home/kali$ 
```

### Create Database Set Permissions
Create database with user just created as the database owner.
```
postgres@kali:/home/kali$ createdb --owner=msf_user my_hacker_db
postgres@kali:/home/kali$ exit
```

Connect Metasploit console (msfconsole) with the new PostgreSQL database by defining the: user, password, host, and database name.

```
msf6 > db_connect <USER>:<ENTER_PASSWORD_HERE>@<HOST>/<DATABASE_NAME>

# example using localhost:
msf6 > db_connect msf_user:password123@127.0.0.1/my_hacker_db
```
> run `db_disconnect` to disconnect

Check status of database:
```
msf6 > db_status
[*] Connected to msf. Connection type: postgresql.
```

Once the database is connected to Metasploit framework (msf), modules can now be stored in the database for faster results. Also the results of system scans and any exploits ran are now stored in the PostgreSQL database.

<hr>

# Terms

**Exploit Code**: code that enters a targeted system taking advantage of a vulnerability

# Sources:
- [Metasploit Project](https://en.wikipedia.org/wiki/Metasploit_Project)
- [Metasploit Framework](https://en.wikipedia.org/wiki/Metasploit_Project#Metasploit_Framework)
- Linux Basics For Hackers
