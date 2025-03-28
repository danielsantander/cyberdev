- [New Project](#new-project)
- [Manage Commands](#manage-commands)
  - [flush](#flush)
  - [migrations](#migrations)
    - [Remove Migrations From SQL](#remove-migrations-from-sql)
    - [Find and remove Migration Files](#find-and-remove-migration-files)
    - [migrate fake-initial](#migrate-fake-initial)
  - [test](#test)
  - [custom management commands](#custom-management-commands)
- [Django Shell](#django-shell)
  - [Reset User Password](#reset-user-password)
  - [Serialize Out Data](#serialize-out-data)
    - [Print Model in JSON format](#print-model-in-json-format)
- [Settings](#settings)
  - [Django Sessions](#django-sessions)
    - [Session settings](#session-settings)
- [Install Apps](#install-apps)

Notes on Django Web Framework and Django Rest Framework.

# New Project

```shell
# Install python packages
python3 -m pip install django
python3 -m pip install djangorestframework

# check Django version
python3 -m django --version

# check Django version alternative
django-admin --version

# Create Project
django-admin startproject {PROJECT_NAME}

# Create App within Project
django-admin startapp {APP_NAME}

# Create Superuser
django-admin createsuperuser
```

The app will be created with the following structure:

```shell
app_name/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

# Manage Commands

## flush

[source -- Django 4.2 ref django-admin flush](https://docs.djangoproject.com/en/4.2/ref/django-admin/#flush)

Flush all data from the database and re-executes any post-synchronization handlers.

```shell
django-admin flush
```

> The already applied migration table is not cleared.
> To start from an empty database and rerun all migrations, it is better to drop and create the database and then run `migrate` instead.

| argument                  | description                                             |
|---------------------------|---------------------------------------------------------|
|   --noinput, --no-input   | Suppresses all user prompts.                            |
|   --database DATABASE     | Specifies the database to flush. Defaults to `default`. |

## migrations

[Django migrations source](https://docs.djangoproject.com/en/4.0/topics/migrations/)

Initial migrations are made for an app and create the first version of the app's tables.

```shell
# make migrations and apply migration
python3 manage.py makemigrations
python3 manage.py migrate

# create empty Migration
python3 manage.py makemigrations {APP_NAME} --name {MIGRATION_FILENAME} --empty

# reverse all migrations for an app
python3 manage.py migrate {APP_NAME} zero

# reverse migration by passing migration number of the app
python3 manage.py migrate {APP_NAME} 0005
```

### Remove Migrations From SQL

Access database: `psql -U <username> <database>`

```sql
-- turn pagination off
\pset pager off

-- list tables
\dt

-- list Django Migration records
SELECT * FROM django_migrations;

-- delete migration table rows for given app:
DELETE FROM django_migrations WHERE app='<app_name>';

-- Drop A Whole Table :)
DROP TABLE <tablename>;
```

### Find and remove Migration Files

```shell
# Find and delete migration files for an app that are not named `__init__.py`.
find src/app_directory/migrations -type f -not -name "__init__.py" -delete
```

### migrate fake-initial

When `migrate --fake-initial` option is used, the initial migrations are treaded specially. Django checks that all tables already exist in the database and fake-applies the migration if so. Without `--fake-initial`, initial migrations are treated no differently from any other migration.

## test

```shell
# Run tests for installed apps.
django-admin test [test_label [test_label ...]]
python3 manange.py test [test_label [test_label ...]]
```

## custom management commands

Can create custom management commands and save within `app/management/commands/ensure_admin.py` then run with `python3 manage.py ensure_user`

Following created by [Eugene Yarmash](https://stackoverflow.com/a/39745576/14745606)

```python
import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--username', help="Admin's username")
        parser.add_argument('--email', help="Admin's email")
        parser.add_argument('--password', help="Admin's password")
        parser.add_argument('--no-input', help="Read options from the environment", action='store_true')

    def handle(self, *args, **options):
        User = get_user_model()

        if options['no_input']:
            options['username'] = os.environ['DJANGO_SUPERUSER_USERNAME']
            options['email'] = os.environ['DJANGO_SUPERUSER_EMAIL']
            options['password'] = os.environ['DJANGO_SUPERUSER_PASSWORD']

        if not User.objects.filter(username=options['username']).exists():
            User.objects.create_superuser(username=options['username'],
                                          email=options['email'],
                                          password=options['password'])
```

> run with: `python manage.py ensure_user --username=admin --email=admin@example.com --password=pass`

# Django Shell

## Reset User Password

Retrieve the desired User object and run the set_password with a new password. Do not forget to save the User object.

```python
from django.contrib.auth.models import User
# or if unknown which User model is being used:
from django.contrib.auth import get_user_model

users = User.objects.all().last()   # desired user object
user.set_password('<enter_new_password>')
user.save()
```

## Serialize Out Data

### Print Model in JSON format

```python
import json
from django.core.serializers import serializer
from myproject.myapp.models import MyModel

# get the object
my_object = MyModel.objects.get(pk=1)

# serialize the object to json
json_data = serialize('json', [my_object])

# load json data into a Python dictionary
data = json.loads(json_data)

# print json data
print(json.dumps(data, indent=4))

# save json data to file
out = open("filename.json", "w")
out.write(json_data)
out.close
```

# Settings

## Django Sessions

The Django session framework supports anonymous and user sessions, which allows storage of arbitrary data for each visitor. Session data is stored on  the server side, and cookies contain the session ID unless the cookie-based session engine is used.

To use sessions, ensure that the `MIDDLEWARE` settings contains:

```python
'django.contrib.sessions.middleware.SessionMiddleware'
```

> it is added by default when creating a new project using the `startproject` command.

Access the current session from the request object using `request.session`

```python
# set a variable in the session
request.session['foo'] =  'bar'

# retrieve a session key
request.session.get('foo')

# delete a key previously stored in session
del request.session['foo']
```

### Session settings

Customize sessions with specific settings such as:

- `SESSION_COOKIE_AGE`: The duration of session cookies in seconds. The default value is 1209600 (two weeks)
- `SESSION_COOKIE_DOMAIN`: The domain used for session cookies. Set this to mydomain.com to enable cross-domain cookies or use None for standard domain cookies.
- `SESSION_COOKIE_SECURE`: A boolean indicating that the cookie should only be sent if the connection is an HTTPS connection
- `SESSION_EXPIRE_AT_BROWSER_CLOSE`: A boolean indicating that the session has to expire when the browser is closed. This is set to False by default, forcing the session duration to the valued stored in the "SESSION_COOKIE_AGE".
- `SESSION_SAVE_EVERY_REQUEST`: A Boolean that, if True, will save the session to the database on every request. The session expiration is also updated each time it's saved.

> Use `request.session.set_expiry()` method to overwrite the duration of the current session.

# Install Apps

Add apps within `INSTALLED_APP` list in settings:

```python
INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    ...
    'rest_framework',
]
```
