# Django Notes

Check version `python -m django --version`

Create project `django-admin startproject mysite` will create the following:
```
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

Run development server `python manage.py runserver`

## Create App
Run the following command to create an app within the Django project.
`python manage.py startapp app_name`

A directory for the app will be created:
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