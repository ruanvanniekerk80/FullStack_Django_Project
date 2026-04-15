from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from django.http import HttpResponse

# This function will create your user when you visit the /setup-admin/ URL


def create_superuser(request):
    username = 'ruan_admin'
    password = 'ChangeThisPassword123!'  # CHANGE THIS IMMEDIATELY AFTER LOGIN
    email = 'admin@example.com'

    try:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            return HttpResponse(f"Superuser '{username}' created successfully!")
        else:
            return HttpResponse("Superuser already exists.")
    except Exception as e:
        return HttpResponse(f"Error: {e}")


urlpatterns = [
    path('admin/', admin.site.urls),

    # This connects everything inside your crm app
    path('', include('crm.urls')),

    # This handles login, logout, password resets, etc.
    path('accounts/', include('django.contrib.auth.urls')),

    # Temporary setup link - visit this ONCE after deploying
    path('setup-admin/', create_superuser),
]
