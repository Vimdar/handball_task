import os
from six.moves.configparser import RawConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECRET_KEY = 's_@dp0qks+r#ziw9ly_8x)a=c=+-f43$g@c$x5a0__mt!!mb^*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'django_filters',
    # registered apps
    'results',
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

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',

    'PAGE_SIZE': 50,
    'ORDERING_PARAM': 'ordering',
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
if os.environ.get('ENVIRONMENT') == 'DOCKER':
    SECRET_KEY = os.environ.get('ENVIRONMENT')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('NAME'),
            'USER': os.environ.get('USER'),
            'PASSWORD': os.environ.get('PASSWORD'),
            'HOST': 'db',
            'PORT': 5432
            # 'OPTIONS': :"{'options': '-c search_path=...'}",
        }
    }
else:
    config = RawConfigParser()
    # move to a better/untracked place or use env variables instead
    config.read(os.path.join(BASE_DIR, 'handball', 'settings.conf'))
    config_section = 'handball_app'
    SECRET_KEY = config.get(config_section, 'SECRET_KEY')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config.get(config_section, 'DATABASE_NAME'),
            'USER': config.get(config_section, 'DATABASE_USER'),
            'PASSWORD': config.get(config_section, 'DATABASE_PASSWORD'),
            'HOST': config.get(config_section, 'DATABASE_HOST'),
            'PORT': config.get(config_section, 'DATABASE_PORT'),
            # 'OPTIONS': :"{'options': '-c search_path=...'}",
        }
    }
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
