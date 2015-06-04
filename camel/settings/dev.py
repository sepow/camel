from .base import * # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data') + 'camel.db',
    }
}

SECRET_KEY = 'a_secret_key'

INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
