Table of Contents
- [Login](#login)
  - [List Users](#list-users)
  - [Set MySQL Password](#set-mysql-password)
- [Databases](#databases)
  - [Show Databases](#show-databases)
  - [Filter Database](#filter-database)
  - [Connect to Database](#connect-to-database)
- [Tables](#tables)
- [Table Columns](#table-columns)
- [Commands](#commands)
  - [SELECT](#select)


Start MySql service
```shell
$ service mysql start
```

# Login
Login with root user on localhost:
```shell
$ mysql -u root -p
```

> The root user's default password configuration is empty, press "ENTER" upon the password prompt.

Login with root user on a remote host:
```shell
$ mysql -u root -p <remote_ip_address>
```

## List Users
Retrieve user, host and password fields from `mysql.user` table.
```sql
SELECT user, host, password FROM mysql.user;
+-------------+-----------+----------+
| User        | Host      | Password |
+-------------+-----------+----------+
| mariadb.sys | localhost |          |
| root        | localhost | invalid  |
| mysql       | localhost | invalid  |
+-------------+-----------+----------+
3 rows in set (0.001 sec)
```

## Set MySQL Password
Set password for root user to `fairbanks123`:
```sql
mysql> UPDATE user SET password = PASSWORD("fairbanks123") where user = 'root';
```


# Databases
## Show Databases
List databases with either `SHOW DATABASES` or `SHOW SCHEMA` which will output the same.

```sql
SHOW DATABASES;
```
```sql
SHOW SCHEMAS;
```

Output: Two default admin databases (`information_schema` & `performance_schema`), and one non-admin database `mysql`.
```sql
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
```

## Filter Database
Use the `LIKE` clause to filter the output given a specific pattern.

Usage: `SHOW DATABASES LIKE <pattern>;

**EXAMPLE**: List databases with names that start with 'open':
```sql
SHOW DATABASES LIKE 'open%';
Empty set (0.000 sec)
```
> percent sign (%) is used to express matching zero, one, or multiple characters.

**EXAMPLE**: List database with `sql` in the name:
```sql
SHOW DATABASES LIKE '%sql%';
+------------------+
| Database (%sql%) |
+------------------+
| mysql            |
+------------------+
```

## Connect to Database
Connect to databases with the `USE` statement.
```sql
USE <database>
```

# Tables
Show tables of a database:
```sql
SHOW TABLES
```

```sql
SHOW TABLES <database>
```

**Example**: Show tables of the `mysql` database:
```sql
SHOW TABLES FROM mysql;
+---------------------------+
| Tables_in_mysql           |
+---------------------------+
| column_stats              |
| columns_priv              |
| db                        |
| event                     |
| func                      |
| general_log               |
| global_priv               |
| gtid_slave_pos            |
| help_category             |
| help_keyword              |
| help_relation             |
| help_topic                |
| index_stats               |
| innodb_index_stats        |
| innodb_table_stats        |
| plugin                    |
| proc                      |
| procs_priv                |
| proxies_priv              |
| roles_mapping             |
| servers                   |
| slow_log                  |
| table_stats               |
| tables_priv               |
| time_zone                 |
| time_zone_leap_second     |
| time_zone_name            |
| time_zone_transition      |
| time_zone_transition_type |
| transaction_registry      |
| user                      |
+---------------------------+
31 rows in set (0.000 sec)
```

# Table Columns
Use the `DESCRIBE` (or `DESC`) statement to display column field information of a given table.

USAGE: `DESCRIBE <table>` or `DESC <table>`
> It's also possible to display table columns with the following command: `SHOW COLUMNS FROM <table>`

**EXAMPLE** List column field information for the `mysql` database table `user`:
```sql
DESCRIBE mysql.user;
+------------------------+---------------------+------+-----+----------+-------+
| Field                  | Type                | Null | Key | Default  | Extra |
+------------------------+---------------------+------+-----+----------+-------+
| Host                   | char(60)            | NO   |     |          |       |
| User                   | char(80)            | NO   |     |          |       |
| Password               | longtext            | YES  |     | NULL     |       |
| Select_priv            | varchar(1)          | YES  |     | NULL     |       |
| Insert_priv            | varchar(1)          | YES  |     | NULL     |       |
| Update_priv            | varchar(1)          | YES  |     | NULL     |       |
| Delete_priv            | varchar(1)          | YES  |     | NULL     |       |
| Create_priv            | varchar(1)          | YES  |     | NULL     |       |
| Drop_priv              | varchar(1)          | YES  |     | NULL     |       |
| Reload_priv            | varchar(1)          | YES  |     | NULL     |       |
| Shutdown_priv          | varchar(1)          | YES  |     | NULL     |       |
| Process_priv           | varchar(1)          | YES  |     | NULL     |       |
| File_priv              | varchar(1)          | YES  |     | NULL     |       |
| Grant_priv             | varchar(1)          | YES  |     | NULL     |       |
| References_priv        | varchar(1)          | YES  |     | NULL     |       |
| Index_priv             | varchar(1)          | YES  |     | NULL     |       |
| Alter_priv             | varchar(1)          | YES  |     | NULL     |       |
| Show_db_priv           | varchar(1)          | YES  |     | NULL     |       |
| Super_priv             | varchar(1)          | YES  |     | NULL     |       |
| Create_tmp_table_priv  | varchar(1)          | YES  |     | NULL     |       |
| Lock_tables_priv       | varchar(1)          | YES  |     | NULL     |       |
| Execute_priv           | varchar(1)          | YES  |     | NULL     |       |
| Repl_slave_priv        | varchar(1)          | YES  |     | NULL     |       |
| Repl_client_priv       | varchar(1)          | YES  |     | NULL     |       |
| Create_view_priv       | varchar(1)          | YES  |     | NULL     |       |
| Show_view_priv         | varchar(1)          | YES  |     | NULL     |       |
| Create_routine_priv    | varchar(1)          | YES  |     | NULL     |       |
| Alter_routine_priv     | varchar(1)          | YES  |     | NULL     |       |
| Create_user_priv       | varchar(1)          | YES  |     | NULL     |       |
| Event_priv             | varchar(1)          | YES  |     | NULL     |       |
| Trigger_priv           | varchar(1)          | YES  |     | NULL     |       |
| Create_tablespace_priv | varchar(1)          | YES  |     | NULL     |       |
| Delete_history_priv    | varchar(1)          | YES  |     | NULL     |       |
| ssl_type               | varchar(9)          | YES  |     | NULL     |       |
| ssl_cipher             | longtext            | NO   |     |          |       |
| x509_issuer            | longtext            | NO   |     |          |       |
| x509_subject           | longtext            | NO   |     |          |       |
| max_questions          | bigint(20) unsigned | NO   |     | 0        |       |
| max_updates            | bigint(20) unsigned | NO   |     | 0        |       |
| max_connections        | bigint(20) unsigned | NO   |     | 0        |       |
| max_user_connections   | bigint(21)          | NO   |     | 0        |       |
| plugin                 | longtext            | NO   |     |          |       |
| authentication_string  | longtext            | NO   |     |          |       |
| password_expired       | varchar(1)          | NO   |     |          |       |
| is_role                | varchar(1)          | YES  |     | NULL     |       |
| default_role           | longtext            | NO   |     |          |       |
| max_statement_time     | decimal(12,6)       | NO   |     | 0.000000 |       |
+------------------------+---------------------+------+-----+----------+-------+
47 rows in set (0.001 sec)

```

> note the following three commands will output the same:
> ```sql
> DESC mysql.user;
> DESCRIBE mysql.user;
> SHOW COLUMNS FROM mysql.user;
> 
> mysql> DESCRIBE user;
> mysql> DESC user;
> mysql> SHOW COLUMNS FROM user;
> ```

# Commands

|  operation  |   description                                       |
|-------------|-----------------------------------------------------|
| `SELECT`    | retrieve data                                       |
| `UNION`     | combine results of two ore more `select` operations |
| `INSERT`    | add/insert new data                                 |
| `UPDATE`    | modify/update existing data                         |
| `DELETE`    | remove/delete data                                  |

## SELECT
Retrieve data from a database table given the column name(s).

Usage: `SELECT <columns> FROM <table>`