FROM python:3

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /usr/src/django/project

EXPOSE 8000