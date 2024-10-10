from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, user_login, profile

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/base.html'), name='logout'),
    path('profile/', profile, name='profile')
]
