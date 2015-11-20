"""
Django settings for Olbizgo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-14)u@f@5d2*lsy8go(+wa!k1=ya=43)2#j#&vv!d(aff@(6-9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',
    'import_export',
    'djangotoolbox',
    'permission_backend_nonrel',
    'ikwen',
    'amazon',
    'cms',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    # 'ikwen.context_processors.project_url',
)

ROOT_URLCONF = 'Olbizgo.urls'

WSGI_APPLICATION = 'Olbizgo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine',
        'NAME': 'olbizgo',
    },
    'umbrella': {
        'ENGINE': 'django_mongodb_engine',
        'NAME': 'ikwen_umbrella',
    }
}

AUTH_USER_MODEL = 'ikwen.Member'

AUTHENTICATION_BACKENDS = (
    'permission_backend_nonrel.backends.NonrelPermissionBackend',
    'ikwen.backends.IkwenAuthBackend',
)

POMMO_DATABASE = ('localhost', 'root', '', '')

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr'

LOCALE_PATHS = (
    '/home/komsihon/Dropbox/PycharmProjects/Olbizgo/locale',
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_ROOT = '/home/komsihon/Dropbox/PycharmProjects/Olbizgo/media/'
MEDIA_URL = 'http://localhost/olbizgo/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = '/home/komsihon/Dropbox/PycharmProjects/Olbizgo/static/'
STATIC_URL = 'http://localhost/olbizgo/static/'

TEMPLATE_DIRS = (os.path.join(BASE_DIR,  'templates'),)
