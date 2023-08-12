- [Prerequisite](#prerequisite)
- [Check Django Version](#check-django-version)
- [Create Project](#create-project)
- [Create App within Project](#create-app-within-project)
- [Create Superuser](#create-superuser)
- [Migrations](#migrations)
  - [Create Empty Migration](#create-empty-migration)
  - [Run Migrations](#run-migrations)
- [Install Apps](#install-apps)
- [Manage Commands](#manage-commands)
  - [flush](#flush)
  - [test](#test)
- [Django Shell](#django-shell)
  - [Get Django User Model](#get-django-user-model)
- [Integrate Redis into Project](#integrate-redis-into-project)

---

Notes on Django Web Framework

# Prerequisite
Install python packages.
```shell
python -m pip install django
python -m pip install djangorestframework
```

# Check Django Version
```shell
python3 -m django --version
```
or
```shell
django-admin --version
```

# Create Project
```shell
django-admin startproject {PROJECT_NAME}
```

# Create App within Project
```shell
django-admin startapp {APP_NAME}
```

A Directory for the app will be created within the project directory:
```
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

# Create Superuser
```shell
django-admin createsuperuser
```

# Migrations
## Create Empty Migration
```shell
python3 manage.py makemigrations {APP_NAME} --name {MIGRATION_FILENAME} --empty
```

## Run Migrations
Run Migrate
```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

# Install Apps
Add apps within `INSTALLED_APP` list in settings:
```python
INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    ...
    'rest_framework',
]
```

# Manage Commands
## flush

[source -- Django 4.2 ref django-admin flush](https://docs.djangoproject.com/en/4.2/ref/django-admin/#flush)

Flush all data from the database and re-executes any post-synchronization handlers.
```shell
django-admin flush
```
> The already applied migration table is not cleared.
>
> To start from an empty database and rerun all migrations, it is better to drop and create the database and then run `migrate` instead.

Args:
| argument                  | description                                             |
|---------------------------|---------------------------------------------------------|
|   --noinput, --no-input   | Suppresses all user prompts.                            |
|   --database DATABASE     | Specifies the database to flush. Defaults to `default`. |

## test
Run tests for installed apps.
```shell
django-admin test [test_label [test_label ...]]
```

#  Django Shell
## Get Django User Model
```python
from django.contrib.auth.models import User

# or if unknown which User model is being used:
from django.contrib.auth import get_user_model
```

# Integrate Redis into Project

Update settings.py file:
```python
```