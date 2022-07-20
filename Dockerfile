# pull official base image
FROM python:3

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apt-get update -y\
    && apt-get install -y python3 \
    && pip install psycopg2-binary

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# run gunicorn
CMD gunicorn SOLUCIONESAGROMINBACKEND.wsgi:application --bind 0.0.0.0:$PORT