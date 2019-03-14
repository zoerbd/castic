FROM python:3.6
MAINTAINER zoerbd
ADD . /var/www/castic
WORKDIR /var/www/castic/src
RUN pip install -r requirements.txt
EXPOSE 8000
CMD exec gunicorn castic.wsgi:application --bind 0.0.0.0:8000 --workers 3
