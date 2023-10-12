FROM python:3.11-slim

ENV APP_HOME=/app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app

COPY deployment/stage-env.local ./config/.env
COPY deployment/docker-entrypoint.sh  docker-entrypoint.sh


RUN ["chmod", "+x", "./docker-entrypoint.sh"]
CMD ["/bin/sh", "./docker-entrypoint.sh"]
