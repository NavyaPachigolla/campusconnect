from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Always open login page first
    path('', lambda request: redirect('login')),

    # Login
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html',
            next_page='role_redirect'
        ),
        name='login'
    ),

    # Logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),

    # Role based redirect
    path('redirect/', views.role_redirect, name='role_redirect'),

    # Core app URLs
    path('', include('core.urls')),
]