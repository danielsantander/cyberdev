# PostgreSQL

Login into database: `psql -U <username> <database>`

Deactivate Pagination: `\pset pager off`

List database tables:
```sql
\dt
```

Drop Tables:
```sql
DROP TABLE <tablename>;
```

Remove (Truncate) data from table:
```sql
TRUNCATE <TableName>, <SecondTableName>;
```