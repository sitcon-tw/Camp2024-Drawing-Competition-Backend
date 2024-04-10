FROM python:3.10.5-alpine

# Authorization
RUN addgroup -S nonroot \
    && adduser -S nonroot -G nonroot
USER nonroot

# Folder
WORKDIR /code
COPY ./ ./code/

# Env
ENV POSTGRES_DB="equipment"
ENV POSTGRES_USER="test"
ENV POSTGRES_PASSWORD="123456"
ENV POSTGRES_DB_URL="127.0.0.1"
ENV POSTGRES_PORT="5432"
ENV POSTGRES_EMAIL="none@gmail.com"

# Dependencies
RUN pip install -r requirements.txt

# Entrypoint
CMD ["python3" "manage.py" "runserver" "0.0.0.0:8000"]