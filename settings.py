from djangoappengine.settings_base import *

import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = '=r-$bi9LA73jc58&9003mmk5ch1k-3d3vfc4(wk0rn3wa1dhvi'

INSTALLED_APPS = (
    'djangoappengine',
    'djangotoolbox',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'userTools',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'views.common_proc',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'