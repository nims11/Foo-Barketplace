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
    'itemTools',
    'searchTools',
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

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),
    os.path.join(os.path.dirname(__file__), 'userTools/templates'),
    os.path.join(os.path.dirname(__file__), 'itemTools/templates'),
    os.path.join(os.path.dirname(__file__), 'searchTools/templates'),
)
try:
    import dbindexer
    DATABASES['native'] = DATABASES['default']
    DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
    INSTALLED_APPS += ('autoload', 'dbindexer',)
    AUTOLOAD_SITECONF = 'dbindexes'
    MIDDLEWARE_CLASSES = ('autoload.middleware.AutoloadMiddleware',) + \
                         MIDDLEWARE_CLASSES
except ImportError:
    pass

DBINDEXER_BACKENDS = ('dbindexer.backends.BaseResolver',
                      'dbindexer.backends.FKNullFix',
                      'dbindexer.backends.InMemoryJOINResolver',
#                      'dbindexer.backends.ConstantFieldJOINResolver',
)

ROOT_URLCONF = 'urls'