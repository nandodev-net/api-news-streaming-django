"""
Django settings for noticias_sin_filtro_server project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

import noticias_sin_filtro_server.tasks as tasks

# -- < App info > ------------------------------------
VERSION = "0.0.1"
DATE_FORMAT = "%y-%m-%d:%H:%M:%S"

# -- < App configuration > ---------------------------
# Compatible client's versions. A version not specified in one of the
# following variables will be considered invalid, and will raise an error

# LAST_VERSION is supported, is the current app version
LAST_VERSION = "v0.0.1"

# versions in COMPATIBLE_UPGRADABLE are supported, but they will issue an update notification
COMPATIBLE_UPGRADABLE = []

# Versions in DEPRECATED_VERSIONS are not supported,
DEPRECATED_VERSIONS = []

# Check that versions are disjoint
assert len({LAST_VERSION, *COMPATIBLE_UPGRADABLE, *DEPRECATED_VERSIONS}) == (
    1 + len(COMPATIBLE_UPGRADABLE) + len(DEPRECATED_VERSIONS)
), "Versions should be unique"

# -- < Init environment variables handler > -------------
import environ

env = environ.Env()
environ.Env.read_env()
# -------------------------------------------------------

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(env("DEBUG", default=1))  # type: ignore

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")  # type: ignore
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS", default="").split(" ") or [] # type: ignore
# Scrapy server
SCRAPY_HOST = env("SCRAPY_HOST", default="http://localhost")  # type: ignore
SCRAPY_PORT = env("SCRAPY_PORT", default="6800")  # type: ignore

# Application definition

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # VSF apps
    "app.scraper.apps.ScraperConfig",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "noticias_sin_filtro_server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "noticias_sin_filtro_server.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env("SQL_ENGINE", default="django.db.backends.sqlite3"),  # type: ignore
        "NAME": env("SQL_DATABASE", default=str(BASE_DIR / "db.sqlite3")),  # type: ignore
        "USER": env("SQL_USER", default="user"),  # type: ignore
        "PASSWORD": env("SQL_PASSWORD", default="password"),  # type: ignore
        "HOST": env("SQL_HOST", default="localhost"),  # type: ignore
        "PORT": env("SQL_PORT", default="5432"),  # type: ignore
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -- < Celery configurations > ------------------------------------------

from celery.schedules import crontab

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://redis:6379") # type: ignore 
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://redis:6379") # type: ignore

CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "noticias_sin_filtro_server.tasks.scraper_task",
        "schedule": crontab(minute="*/1"),
    }
}

# -- < Rest framework configurations > ----------------------------------
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_VERSION": "v0.0.1",
    "ALLOWED_VERSIONS": ["v0.0.1"],
}
