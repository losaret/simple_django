from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import Registration_view

app_name = "user_profile"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name='login'),
    path("logout/", auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path("registration/", Registration_view, name='registration')
]