"""
Django settings for Productivity Project Management System
Author: Ani
"""

from pathlib import Path
import os
import dj_database_url
import pymysql

BASE_DIR = Path(__file__).resolve().parent.parent

pymysql.install_as_MySQLdb()

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-this-to-a-secure-key")
DEBUG = os.getenv("DEBUG", "True") == "True"

# --------------------------------------------------------
# HOST CONFIGURATION
# --------------------------------------------------------
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "pms-t7l8.onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://pms-t7l8.onrender.com",
]

RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# --------------------------------------------------------
# APPLICATIONS
# --------------------------------------------------------
INSTALLED_APPS = [
    # Django Core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "django.contrib.sites",

    # Allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    # Project Apps
    "accounts",
    "projects",
    "tasks",
    "dashboard",
    "communications",
    "design",
    "notifications",

    # WebSocket Channels
    "channels",
]

SITE_ID = 1

# --------------------------------------------------------
# AUTH & USER MODEL
# --------------------------------------------------------
AUTH_USER_MODEL = "accounts.CustomUser"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_URL = "/user/login/"
LOGOUT_REDIRECT_URL = "/user/login/"
LOGIN_REDIRECT_URL = "/dashboard/global/"
ACCOUNT_SIGNUP_REDIRECT_URL = "/dashboard/"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_SIGNUP_FIELDS = ["email", "username", "password1", "password2"]
ACCOUNT_LOGIN_METHODS = {"username", "email"}

SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_ADAPTER = "accounts.adapters.CustomSocialAccountAdapter"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "online",
            "prompt": "select_account",
        },
    }
}

# --------------------------------------------------------
# CHANNELS
# --------------------------------------------------------
ASGI_APPLICATION = "backend.asgi.application"
CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
}

# --------------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

# --------------------------------------------------------
# TEMPLATES
# --------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "backend.wsgi.application"

# --------------------------------------------------------
# DATABASE (MySQL Local / PostgreSQL Render)
# --------------------------------------------------------
if os.getenv("RENDER"):  # When deployed on Render
    DATABASES = {
        "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "productivity_db",
            "USER": "root",
            "PASSWORD": "root",
            "HOST": "localhost",
            "PORT": "3306",
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# --------------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------
# STATIC & MEDIA FILES
# --------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------------
# EMAIL
# --------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
