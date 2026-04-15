from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # This connects everything inside your crm app
    path('', include('crm.urls')),

    # This handles login, logout, password resets, etc.
    path('accounts/', include('django.contrib.auth.urls')),
]
