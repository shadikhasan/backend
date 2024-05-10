# urls.py
from django.urls import path
from . import views
from core.views import *
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', UserLogInView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password')
]
