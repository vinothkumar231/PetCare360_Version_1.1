"""
WSGI config for petcare360 project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""
import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "petcare360.settings")
django.setup()

# WSGI entrypoint should not create users or run migrations automatically.
# Use manage.py or populate_demo.py to seed sample data safely.
application = get_wsgi_application()
app = application
