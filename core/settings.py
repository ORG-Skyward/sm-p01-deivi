"""
Django settings for core project.
"""

import os
from pathlib import Path
import dj_database_url
from django.db.backends.mysql.base import DatabaseWrapper

# Desactiva la restricción estricta de versión de MySQL para que acepte versiones 8.0+
DatabaseWrapper.check_database_version_supported = lambda self: None

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-7b^o#@g^8)1!u$af+u7$x4-)5i%kn#6pc^$63w5)pwhwr@r4ck'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'calculadora',
    'tienda',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Middleware de WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['calculadora/templates/calculadora', 'tienda/templates/tienda'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Configuración de Bases de Datos (CI vs Local vs Producción en Render con Neon)
if os.getenv("CI"):
    # En GitHub Actions usamos SQLite en memoria para que las pruebas pasen sin requerir servidores externos
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    DATABASES = {
        'default': {  # PostgreSQL (Local / pgAdmin)
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'proyecto',
            'USER': 'postgres',
            'PASSWORD': 'root',
            'HOST': 'localhost',
            'PORT': '5432',
        },
        'mysql_db': {  # MySQL (Local)
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'proyecto_mysql',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }

    # Si estamos en Render (o existe la variable DATABASE_URL), se sobrescribe 'default' con Neon en la nube
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        DATABASES['default'] = dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            ssl_require=True
        )

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos Estáticos (CSS, JS, etc.)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Configuración para archivos multimedia (Portadas de videojuegos)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}