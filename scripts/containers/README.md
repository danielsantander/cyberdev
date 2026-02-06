Dockerized Applications

- [Django Application](#django-application)
- [nginx with Ubuntu24](#nginx-with-ubuntu24)

---

# Django Application

Prerequisites:

- Environment variables set within `dockerfiles/django/container.env`
- Django app within `dockerfiles/django/app`
- `python3 manage makemigrations` is already run and database `dockerfiles/django/app/db.sqlite3` exists

Building and running Django application:

```shell
./run.sh django
```

Once running, navigate to `http://0.0.0.0:8000/admin/` and log in using credentials from `dockerfiles/django/container.env`

# nginx with Ubuntu24

```shell
./run.sh ubuntu
```