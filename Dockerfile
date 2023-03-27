FROM python:3.9-alpine3.13
LABEL maintainer="christojohnsonv@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000
ARG DEV=false
RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
      build-base postgresql-dev musl-dev zlib zlib-dev && \
  pip install -r /tmp/requirements.txt && \
  pip install -r /tmp/requirements.dev.txt && \
  rm -rf /tmp && \
  apk del .tmp-build-deps && \
  adduser \
    --disabled-password \
    --no-create-home \
    django-user

USER django-user
