"""
WSGI config for DRF project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('VERSION', '1.0.8')

if os.environ['VERSION'] == '1.0.0':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF.settings.production')
elif os.environ['VERSION'] == '1.0.1':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF.settings.production')
elif os.environ['VERSION'] == '1.0.2':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF.settings.production')
elif os.environ['VERSION'] == '1.0.5':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF.settings.production')
elif os.environ['VERSION'] == '1.0.6':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF.settings.production')
elif os.environ['VERSION'] == '1.0.7':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF.settings.production')
elif os.environ['VERSION'] == '1.0.8':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF.settings.production')


application = get_wsgi_application()
