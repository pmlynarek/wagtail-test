FROM python:3.7.3

RUN apt-get update && apt-get install -y postgresql-client-9.6

RUN pip install --upgrade pip

RUN mkdir /app
ADD . /app/
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
