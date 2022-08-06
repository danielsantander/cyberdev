# Django Migrations

[Django migrations source](https://docs.djangoproject.com/en/4.0/topics/migrations/)

Initial migrations are made for an app and create the first version of the app's tables.

When `migrate --fake-initial` option is used, the initial migrations are treaded specially. Django checks that all tables already exist in the database and fake-applies the migration if so. Without `--fake-initial`, initial migrations are treated no differently from any other migration.

# Make Migrations
Run `makemigrations` command for Django to write a new set of migrations.
```shell
python3 manage.py makemigrations

# or for specific app:
python3 manage.py makemigrations your_app_label
```

Apply the newly added migrations with the `migrate` command.
```shell
python3 manage.py migrate'
```

# Reverse Migrations
Reverse migrations by passing the migration number of the previous migration.

Example: reverse to migration post.0005
```shell
python3 manage.py migrate post 0005
  Target specific migration: 0005_auto, from blogs
Running migrations:
  Rendering model states... DONE
  Unapplying post.0006_auto... OK
```

Revers **all** migrations applied for an app with the `zero` argument
```shell
python3 manage.py migrate blog zero
Operations to perform:
  Unapply all migrations: blog
Running migrations:
  Rendering model states... DONE
  Unapplying blog.0002_auto... OK
  Unapplying blog.0001_initial... OK
```

# Remove Tables/Migrations in PostgreSQL Database

Access database: `psql -U <username> <database>`

List Tables
```sql
\pset pager off
\dt
```

List Django Migration Records:
```sql
SELECT * FROM django_migrations;
```

Delete migration table rows for given app:
```sql
DELETE FROM django_migrations WHERE app='<app_name>';
```

Drop A Whole Table:
```sql
DROP TABLE <tablename>;
```

