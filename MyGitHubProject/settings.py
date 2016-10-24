"""
Django settings for MyGitHubProject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&a!xdbo0wzujlu^k8t3ecqyr@u0_#lt@nn+3(s$ctv*q36&h*m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ADMINS = 'Hendrik', 'hendrikdw@mycomax.com'

MEDIA_URL = '/site_media/'
MEDIA_ROOT = MEDIA_URL

MEDIA_URL = 'static/'

# Static files URL
STATIC_ROOT = os.path.join(BASE_DIR, 'MyGitHubProject/dummy_static/')
MY_STATIC_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'static/')

MY_STATIC_URL = '/static/'
STATIC_URL = MY_STATIC_URL

# Locations of static files

STATICFILES_DIRS = (
    MY_STATIC_ROOT,
)

ALLOWED_HOSTS = ['*']

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'MyGitHubProject.Issues',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.debug",
    #"django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'MyGitHubProject.urls'

WSGI_APPLICATION = 'MyGitHubProject.wsgi.application'

TEMPLATE_DIRS = (
    '/Django/MyGitHubProject/templates',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

# Caching

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211'
    }
}
CACHE_MIDDLEWARE_KEY_PREFIX = ''
CACHE_MIDDLEWARE_ALIAS = 'MyGitHubProject'
#SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'


LANGUAGE_CODE = 'en-ZA'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_L10N = False

USE_TZ = False

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'



