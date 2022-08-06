# DJANGO

Notes on Django Web Framework

## Check Django Version

```shell
python3 -m django --version
```
or
```shell
django-admin --version
```

## Create Project
```shell
django-admin startproject <project_name>
```

## Create App within Project
```shell
python3 manage.py startapp <app_name>
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