  
from .base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'bfc)l6*m_50w#yfv6nhq@t(v6gs6pjlgi4jux5!)8oktaldhm1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

STATIC_ROOT = os.path.join(BASE_DIR,'static')
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


