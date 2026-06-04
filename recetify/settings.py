import os
from pathlib import Path
from dotenv import load_dotenv

from django.utils.translation import gettext_lazy as _

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

ENVIRONMENT = os.getenv("ENVIRONMENT", "local")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("RECETIFY_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False") == "True"

if ENVIRONMENT == "production":
    ALLOWED_HOSTS = [
        "recetify.online",
        "www.recetify.online",
        "46.101.167.180"
    ]
else:
    ALLOWED_HOSTS = [
        "127.0.0.1",
        "localhost"
    ]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # External apps
    "modeltranslation",
    "tailwind",
    "theme",
    "django_browser_reload",
    "rosetta",
    
    # My apps
    "recipes.apps.RecipesConfig",
    "profiles.apps.ProfilesConfig",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware", # i18n
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "recetify.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n", # i18n

                # My context processors
                "profiles.context_processors.user_profile"
            ],
        },
    },
]

WSGI_APPLICATION = "recetify.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if ENVIRONMENT == "production":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "es"

TIME_ZONE = "Europe/Madrid"

USE_I18N = True
USE_L10N = True
USE_TZ = True
PREFIX_DEFAULT_LANGUAGE = True

LANGUAGES = [
    ('es', _('Español')),
    ('en', _('Inglés')),
]

LANGUAGE_COOKIE_NAME = "django-language"

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

ROSETTA_AUTO_COMPILE = True

MODELTRANSLATION_DEFAULT_LANGUAGE = 'es'  

# Pestañas bonitas en el admin
MODELTRANSLATION_ADMIN = True

MODELTRANSLATION_AUTO_POPULATE = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "theme" / "static",
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TAILWIND_APP_NAME = "theme"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGOUT_REDIRECT_URL = "home"

LOGIN_URL = '/login/'
