"""
WSGI config for crm_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command # Required to run migrations

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

application = get_wsgi_application()

# Vercel-specific alias
app = application

# Run migrations automatically on startup
# This fixes the "relation auth_user does not exist" error
try:
    print("Checking for database migrations...")
    call_command('migrate', interactive=False)
    print("Migrations completed successfully.")
except Exception as e:
    print(f"Migration error: {e}")