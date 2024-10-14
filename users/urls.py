# juliana/urls.py
from django.urls import path, include

urlpatterns = [
    # Other URLs for your app
    path('accounts/', include('allauth.urls')),  # Includes all Allauth views and URLs
]
