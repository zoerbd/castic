"""
Django settings for webmanagement project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os, json, subprocess
from django.shortcuts import redirect
from django.utils.timezone import now

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_e$7#$+ox!@5+&5hj&njc)21c=3e8=@(k1b@%2vou)v5ks8joz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
		'localhost'
		]


# Application definition

INSTALLED_APPS = [
    'index',
    'login',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webmanagement.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/var/www/castic/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webmanagement.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'castic',
        'USER': 'postgres',
        'PASSWORD': 'AllgemeineAblage',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------>
# ---- Globally used config-vars and function defined here ---

# read config file
with open('config.json') as jsonFile:
        config = json.load(jsonFile)

def __shell__(command):
        '''
        This function makes it less pain to get shell answers
        '''
        return subprocess.check_output(command, shell=True).decode('utf-8')
       
def __log__(msg):
    # if empty argument given, no error occurred
    if not msg:
        return

    # document and return
    print(msg)
    with open('castic.log', 'a') as logfile:
        logfile.write('{} - {}'.format(now(), msg))
    return msg

def loginRequired(func):
    '''
    Basic decorator to apply on views to require user to be logged in.
    '''
    def wrapper(*args, **kwargs):
        if not args[0].user.is_authenticated:
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper

def getVersion():
    '''
    Returns current version.
    '''
    return '0.6.2'
# ------------------------------------------------------------>