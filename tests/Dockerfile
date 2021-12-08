FROM python:3.9.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /tests

WORKDIR /tests

COPY . /tests

RUN pip3 install -r requirements.txt