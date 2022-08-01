from .common import *

DEBUG = True
SECRET_KEY = 'django-insecure-2=eczm%_m1kgdu$#h0w&*9m^cyi^*=l(u4!079v=r5yct7^)93'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront3',
        'HOST': 'mysql',
        'USER': 'root',
        'PASSWORD': 'MyPassword'
    }
}

CELERY_BROKER_URL = 'redis://redis:6379/1'
CELERY_BEAT_SCHEDULE = {
    'notify_customer': {
        'task': 'playground.tasks.notify_customer',
        'schedule': 10,
        'args': ['Hello World']
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp4dev'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = 'no-reply@storefront.com'

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}
