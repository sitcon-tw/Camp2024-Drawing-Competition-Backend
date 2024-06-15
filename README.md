# Drawing Competition Backend

---

## Prerequisite

- Python 3.10.5
- Poetry

---

## Getting Start - API Server

### Init Env

```shell
poetry install # Install Dependencies
poetry shell # In Project root
```

### Migrate Database

```shell
python manage.py makemigrations # Check Model Context modification
python manage.py migrate # Migrate Migrations to Database
```

### Run Server

```shell
python manage.py runserver [0.0.0.0:8000] # Run Server
# 0.0.0.0:8000 mean output to all IP
```

### Run Server HTTPS Dev Mode

```python
python manage.py runserver_plus --key-file selftest-key --cert-file selftest-cert 0.0.0.0:8000
```

---

## Getting Start MQTT Publisher

### Init Env

```shell
poetry shell # In Project root
python manage.py migrate django_celery_beat
```

### Run Publisher

```shell
celery -A backend worker --loglevel=info
```