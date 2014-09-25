# Django settings for camel project.

import os
SITE_ROOT = os.path.dirname(os.path.dirname(__file__))
TEX_ROOT  = os.path.join(SITE_ROOT, 'tex/')
XLS_ROOT  = os.path.join(SITE_ROOT, 'xls/')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zm8*_50*9-sziwme0*@n*^zb=g&(r^wwft5#q+me-345z=377*'

# settings for development server
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = []
# end settings for development server

# settings for production server 
# should also set log-level to INFO or ERROR
# DEBUG = False
# TEMPLATE_DEBUG = DEBUG
# ALLOWED_HOSTS = [camel.maths.cf.ac.uk]
# end settings for development server

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'camel',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'camel.urls'
WSGI_APPLICATION = 'camel.wsgi.application'


# database: development
DATABASES = {
	'default': {
    	'ENGINE': 'django.db.backends.sqlite3', 
    	'NAME': os.path.join(SITE_ROOT, 'data') + '/camel.db',
	}		
}

# database: production
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'camel',
#	'USER': 'humpty',
#	'PASSWORD': '12345',
#	'HOST': 'localhost',
#	'PORT': '',
#    }
#}

# location
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# media (user uploaded)
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
MEDIA_URL = ''

# static files (css, js, png)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'staticfiles')
STATICFILES_DIRS = (
	os.path.join(SITE_ROOT, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# templates
TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# redirect
LOGIN_URL = '/login/'

