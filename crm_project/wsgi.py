import os
import sys
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import get_user_model

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

# Initialize the Django Application
application = get_wsgi_application()

# --- THE AUTO-ADMIN SECTION ---
# This code runs on Vercel to ensure your superuser always exists in Neon
try:
    User = get_user_model()

    # This grabs the password you set in the Vercel "Environment Variables"
    # If not found, it uses the fallback password below
    env_password = os.environ.get(
        'DJANGO_SUPERUSER_PASSWORD', 'ChangeThisPassword123!')

    username = 'ruan_admin'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email='admin@example.com',
            password=env_password
        )
        print(f"✅ Superuser '{username}' created successfully!")
    else:
        # If the user exists, this ensures the password matches your Vercel setting
        u = User.objects.get(username=username)
        u.set_password(env_password)
        u.is_superuser = True
        u.is_staff = True
        u.save()
        print(f"🔄 Superuser '{username}' updated successfully.")

except Exception as e:
    # This prevents the site from crashing if the database isn't ready yet
    print(f"⚠️ Admin setup skipped: {e}")
