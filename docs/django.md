- [New Project](#new-project)
- [Manage Commands](#manage-commands)
  - [flush](#flush)
  - [migrations](#migrations)
  - [test](#test)
- [Django Shell](#django-shell)
  - [Reset User Password](#reset-user-password)
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

```shell
# Create Empty Migration
python3 manage.py makemigrations {APP_NAME} --name {MIGRATION_FILENAME} --empty

# create and run migrations
python3 manage.py makemigrations
python3 manage.py migrate

# reverse all migrations for an app
python3 manage.py migrate {APP_NAME} zero

```

## test

```shell
# Run tests for installed apps.
django-admin test [test_label [test_label ...]]
python3 manange.py test [test_label [test_label ...]]
```

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

## Print Model in JSON format

```python
import json
from django.core.serializers import serializer

# Get your object
my_object = MyModel.objects.get(pk=1)

# Serialize the object to JSON
json_data = serialize('json', [my_object])

# Load the JSON data into a Python dictionary
data = json.loads(json_data)

# Print the JSON data
print(json.dumps(data, indent=4))
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
