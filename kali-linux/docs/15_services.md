
- [Manage Services](#manage-services)
  - [List Services](#list-services)
- [Apache Web Server](#apache-web-server)
  - [Install Apache](#install-apache)
  - [Start Server](#start-server)
  - [Configure Web Server](#configure-web-server)
- [OpenSSH](#openssh)
- [MySQL](#mysql)
- [PostgreSQL](#postgresql)

# Manage Services
A service is a program or application that runs in the background waiting to be used. Manage these services through the command line.

Usage: `service <service_name> <start|stop|restart>`

```shell
# start service
$ service <service_name> start

# stop service
$ service <service_name> stop

# restart service to capture any new configuration changes made
$ service <service_name> restart
```

## List Services

```
# list all available services
service --status-all | grep "+";

# list all services currently running
service --status-all | grep "+";
```

# Apache Web Server
A free and open-source Web server software created by American software developer Robert McCool. Apache was released in 1995.

## Install Apache
> Apache comes already installed on Kali Linux and many other Linux distros.

```shell
$ apt-get install apache2
```

## Start Server
Start Apache daemon. Once started, the default web page can be accessed at http://localhost/
```shell
$ sudo services apache2 start
```

## Configure Web Server

Apache's default index page is located at `/var/www/html/index.html`. Edit this page to server up anything you would like.

**Example**: With a text editor, create a new default web page with the following HTML.
> save the following in `/var/www/html/index.html`
```html
<html>
  <body>
    <h1>Homepage</h1>
    <p>This is the new default web page.</p>
  </body>
</html>
```
> note if the page is not updating, try restarting the Apache2 service `sudo service apache2 restart`

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
