# PostgreSQL

Login: `psql -U <username> <database>`

Deactivate Pagination: `\pset pager off`

List database tables: `\dt`

List User Info: `\du`

Drop Tables: `sql
DROP TABLE <tablename>;
```

Remove (Truncate) data from table:
```sql
TRUNCATE <TableName>, <SecondTableName>;
```

# Create Database
Create a database named "mydb".
```sql
CREATE DATABASE mydb;
```

# Create Postgres User (MacOS)
If on MacOS and installed postgres through Homebrew, create `postgres` user by running the following:
```shell
/usr/local/opt/postgres/bin/createuser -s postgres
```

# Set Password
Set the password for the postgres user — by default, it has no password.
```sql
postgres=# \password postgres
```

# Associate User With Database
Create a root user with admin privileges. Login to create a user that will have privileges to create and manage databases within the service.
```sql
CREATE ROLE newUser WITH LOGIN PASSWORD ‘password’;
ALTER ROLE newUser CREATEDB;
```

Grant user access to a database named "mydb".
```sql
GRANT ALL PRIVILEGES ON DATABASE mydb TO <username>;
```