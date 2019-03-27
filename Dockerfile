FROM python:3.7-alpine
MAINTAINER Jesus Munoz

# It's recommended setup python in unbuffered mode when installed on docker to avoid problems
ENV PYTHONUNBUFFERED 1

# Copy requirements in docker image
COPY requirements.txt /requirements.txt

# Postgres libraries with minimun extra dependencies so packages in requirements dont fail
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps\
        gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

# Afer requirements installation we can delete the temporary requirements
RUN apk del .tmp-build-deps

# Create an empty folder in our docker container and switches this folder as default location
# Copies the project to the default docker folder
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Create a user that is going to be used to run applications only
# Security propuses an avoid docker run processes with root privileges
RUN adduser -D user
USER user
