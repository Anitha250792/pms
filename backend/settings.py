"""
Django settings for Productivity Project Management System
Author: Ani
Framework: Django + MySQL + Bootstrap
"""

from pathlib import Path
import os
import pymysql
pymysql.install_as_MySQLdb()

# --------------------------------------------------------
# BASE CONFIGURATION
# --------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-to-a-secure-key'
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
 # e.g. ['127.0.0.1', 'localhost']


# --------------------------------------------------------
# APPLICATIONS
# --------------------------------------------------------
INSTALLED_APPS = [
    # Django Core Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    # Project Apps
    'accounts',
    'projects',
    'tasks',
    'dashboard',
    
]

# --------------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

# --------------------------------------------------------
# TEMPLATES
# --------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ global templates folder
        'APP_DIRS': True,                  # ✅ enables app templates
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

WSGI_APPLICATION = 'backend.wsgi.application'


# --------------------------------------------------------
# DATABASE (MySQL)
# --------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'productivity_db',
        'USER': 'root',            # change if needed
        'PASSWORD': 'root',            # enter your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}


# --------------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------------
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


# --------------------------------------------------------
# AUTHENTICATION SETTINGS
# --------------------------------------------------------
AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = 'accounts:login'

# --------------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# --------------------------------------------------------
# STATIC & MEDIA FILES
# --------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --------------------------------------------------------
# SECURITY & PERFORMANCE (for deployment)
# --------------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000'
]

SESSION_COOKIE_AGE = 3600  # 1 hour session
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --------------------------------------------------------
# EMAIL CONFIGURATION (for notifications)
# --------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# For production, you can use SMTP:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'ntanithasaravanan@gmail.com'
# EMAIL_HOST_PASSWORD = 'xwlx kmjf aagb berd'
