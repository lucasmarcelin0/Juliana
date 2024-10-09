from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.login_view, name='default'),  # Make this the default view for '/users/'
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('register/', views.register_view, name='register'),  # Register view
]
