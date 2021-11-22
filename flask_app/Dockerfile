FROM python:3.9.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /flask_app

WORKDIR /flask_app

COPY . /flask_app

RUN pip3 install -r requirements.txt
