from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db6vul6kprvsjc',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': 5432,

        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'db6vul6kprvsjc',
        #'USER': 'u1ip2acl0kiigt',
        #'PASSWORD': 'pfb877fa602c6fc204bf6dd9ad72555384fd2c9998b75f2c086fbb4847e0f7bf0',
        #'HOST': 'ec2-18-210-92-196.compute-1.amazonaws.com',
        #'PORT': 5432,
    }
}


STATIC_URL = '/static/'