FROM python:3.6
MAINTAINER zoerbd
ADD . /var/www/castic
WORKDIR /var/www/castic
RUN pip install -r requirements.txt
EXPOSE 8000
CMD exec gunicorn webmanagement.wsgi:application --bind 0.0.0.0:8000 --workers 3
