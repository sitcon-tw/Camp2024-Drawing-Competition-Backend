# Drawing Competition Backend

---

## Prerequisite

- Python 3.9.1
- Poetry

---

## Getting Start - API Server

### Init Env

```shell
poetry shell # In Project root
```

### Migrate Database

```shell
python manage.py migrate
```

### Run Server

```shell
python manage.py runserver
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