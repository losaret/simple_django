
from .settings import * 

DEBUG = True

SECRET_KEY = "mega-super-secret-key"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MIGRATION_MODULES = {}