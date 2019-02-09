FROM python:3.6
MAINTAINER zoerbd
ADD . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD exec gunicorn webmanagement/wsgi.py:application --bind 0.0.0.0:8000 --workers 3
