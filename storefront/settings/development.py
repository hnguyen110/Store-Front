from .common import *

DEBUG = True
SECRET_KEY = 'django-insecure-2=eczm%_m1kgdu$#h0w&*9m^cyi^*=l(u4!079v=r5yct7^)93'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': ''
    }
}
