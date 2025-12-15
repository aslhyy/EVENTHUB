from .base import *
import os
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["*"],

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

import logging
logging.getLogger(__name__).info("🚀 Settings PROD cargados en Koyeb")


SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

APPEND_SLASH = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
