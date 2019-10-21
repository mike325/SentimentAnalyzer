# pull official base image
FROM python:3.7.4-alpine

ENV PROJECT_NAME sentiment

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/${PROJECT_NAME}

# set work directory
WORKDIR /usr/src/${PROJECT_NAME}

# Install psycopg2 and mysqlclient
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev postgresql-dev \
    && apk add mysql-client \
    && addgroup mysql mysql \
    && pip install --upgrade pip \
    && pip install mysqlclient \
    && apk del build-deps

# install dependencies
COPY requirements/ .
RUN pip install -r requirements/requirements.txt

# Copy project
COPY . /usr/src/${PROJECT_NAME}

EXPOSE 8000

STOPSIGNAL SIGINT

RUN python manage.py collectstatic --noinput --clear

ENTRYPOINT ["python", "manage.py"]

CMD ["runserver", "0.0.0.0:8000"]
