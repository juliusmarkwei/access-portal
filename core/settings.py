from pathlib import Path
from decouple import config
from datetime import timedelta
import os
import django_heroku
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["access-portal-client.vercel.app"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "djoser",
    "src.key",
    "src.user",
    "api",
    "corsheaders",
    "drf_spectacular",
    "whitenoise",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

AUTH_USER_MODEL = "user.User"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# JWT CONFIGURATIONS
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# DJOSER CONFIGURATIONS
DJOSER = {
    "SERIALIZERS": {
        "user_create_password_retype": "src.user.serializers.UserCreateSerializer",
        "user": "src.user.serializers.UserSerializer",
        "current_user": "src.user.serializers.UserSerializer",
    },
    "PASSWORD_RESET_CONFIRM_URL": "reset-password/?uid={uid}&token={token}",
    "ACTIVATION_URL": "user-activate/?uid={uid}&token={token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "USER_CREATE_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "LOGIN_FIELD": "email",
}

SITE_NAME = config("SITE_NAME")
DOMAIN = config("DOMAIN")

# EMAIL CONFIGURATIONS
EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_USE_TLS = config("EMAIL_USE_TLS")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://access-portal-client.vercel.app",
]


# CELERY SETTINGS
CELERY_BROKER_URL = config("CELERY_BROKER_URL")

CELERY_BEAT_SCHEDULE = {
    "expire-access-keys": {
        "task": "api.tasks.expire_access_keys",
        "schedule": 600,  # Run every 10 minutes (600 seconds)
    },
}

# DRF-SPECTACULAR CONFIGURATIONS
SPECTACULAR_SETTINGS = {
    "TITLE": "Access Portal API Documentation ©️",
    "DESCRIPTION": "Our project is a secure access key management system designed to streamline the process of granting and managing access keys for users. It allows users to request, view, and manage their access keys, while administrators have the ability to grant, revoke, and monitor access keys. The system ensures data integrity and security by enforcing access key validity periods and providing granular control over access permissions. Built using Django and Django REST Framework, our solution offers a user-friendly interface and robust backend functionality to meet the access management needs of modern organizations",
    "VERSION": "1.0.0",
    "SERVE_URLCONF": "core.urls",
    "SERVE_PUBLIC": True,
    "SERVE_INCLUDE_SCHEMA": False,
    "CONTACT": {"name": "Julius Markwei", "email": "julius.markwei@stu.ucc.edu.gh"},
}

# Heroku CONFIGURATION
django_heroku.settings(locals())
