# ARG PY_VERSION=3.7
# FROM python:${PY_VERSION}-slim as builder

FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

# creates a fresh handball_app database and users/passwords
COPY init.sql /docker-entrypoint-initdb.d/

RUN mkdir /django-docker
WORKDIR /django-docker
ADD requirements.txt /django-docker/
RUN pip install -r requirements.txt
ADD . /django-docker

