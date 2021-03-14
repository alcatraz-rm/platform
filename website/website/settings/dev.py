from .base import *


DEBUG = True

SECRET_KEY = "i4$gu2p8^5=f33&z35y63+$0-ze9%=0xgkw0-0zc4&16(qi3xu"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "website_data",
        "USER": DATABASE_USER,
        "PASSWORD": DATABASE_PASSWORD,
        "HOST": "localhost",
        "PORT": "",
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {"console": {"class": "logging.StreamHandler", },
                 "file": {"level": "DEBUG", "class": "logging.FileHandler",
                          "filename": os.path.join('logs', 'debug_log.log'), "formatter": "verbose"}, },
    "root": {"handlers": ["console", "file"], "level": "INFO", },
    "loggers": {
        "django": {"handlers": ["console", "file"], "level": "INFO",
                   "propagate": False, },
        "django.db_backends": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.db": {"handlers": ["console", "file"], "level": "DEBUG",
                      "propagate": False, },
    },
}
