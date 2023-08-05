
- [OpenSSH](#openssh)
- [MySQL](#mysql)
- [PostgreSQL](#postgresql)

# OpenSSH
*Secure Shell* (SSH) is used to securely connect to a remote system. SSH enables:
- creating a user access list
- authentication with encrypted passwords
- communication encryption

```shell
# start ssh service
$ service ssh start
```

SSH into the machine
```shell
$ ssh <user>@<ip_address>
password:
```

# MySQL
Learn more from [MySQL docs](MySQL.md)

Start services and login to MySQL:
```bash
# start MySQL
$ service mysql start

# login, when prompted for password press "ENTER"
$ mysql -u root -p

# view databases:
mysql> SHOW DATABASES;

# view users from `mysql` database and `user` table:
mysql> SELECT user, host, password FROM mysql.user;
```

> may need to use sudo command as such: `sudo mysql -u root -p`


# PostgreSQL
