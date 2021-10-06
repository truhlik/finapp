FROM python:3.7.3-slim-stretch
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libgdal-dev curl

RUN mkdir /app
WORKDIR /app

COPY requirements/* /app/requirements/
RUN ls /app/requirements/
RUN pip install -r /app/requirements/local.pip

COPY . /app/
