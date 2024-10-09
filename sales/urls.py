from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'sales'  # This sets the namespace for the app

urlpatterns = [
    path("", views.index, name="index"),
    path("perfil/", views.perfil, name="perfil"),
    path('filter_properties/', views.filter_properties, name='filter_properties'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
