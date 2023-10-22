- [Prerequisite](#prerequisite)
- [Check Django Version](#check-django-version)
- [Create Project](#create-project)
- [Create App within Project](#create-app-within-project)
- [Create Superuser](#create-superuser)
- [Migrations](#migrations)
  - [Create Empty Migration](#create-empty-migration)
  - [Run Migrations](#run-migrations)
  - [Reverse All Migrations For An App](#reverse-all-migrations-for-an-app)
- [Install Apps](#install-apps)
- [Manage Commands](#manage-commands)
  - [flush](#flush)
  - [test](#test)
- [Django Shell](#django-shell)
  - [Get Django User Model](#get-django-user-model)
- [Django Sessions](#django-sessions)
  - [Session settings](#session-settings)
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
Create migrations.
```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

## Reverse All Migrations For An App
```shell
python3 manage.py migrate {APP_NAME} zero
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
# or
python3 manange.py test [test_label [test_label ...]]
```

#  Django Shell
## Get Django User Model
```python
from django.contrib.auth.models import User

# or if unknown which User model is being used:
from django.contrib.auth import get_user_model
```

 # Django Sessions
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

# delete a key previously stored in sessino
del request.session['foo']
```

## Session settings
Customize sessions with specific settings such as:
- `SESSION_COOKIE_AGE`: The duration of session cookies in seconds. The default value is 1209600 (two weeks)
- `SESSION_COOKIE_DOMAIN`: The domain used for session cookies. Set this to mydomain.com to enable cross-domain cookies or use None for standard domain cookies.
- `SESSION_COOKIE_SECURE`: A boolean indicating that the cookie should only be sent if the connection is an HTTPS connection
- `SESSSION_EXPIRE_AT_BROWSER_CLOSE`: A boolean indicating that the session has to expire when the browser is closed. This is set to False by default, forcing the session duration to the valued stored in the "SESSION_COOKIE_AGE".
- `SESSSION_SAVE_EVERY_REQUEST`: A Boolean that, if True, will save the session to the database on every request. The session exipiration is also updated each time it's saved.

> Use `request.session.set_expiry()` method to overwrite the duration of the current session.


# Integrate Redis into Project
Update settings.py file:
```python
```