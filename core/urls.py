from django.urls import path, include
from .views import UserRegistrationView, UserLogInView, UserProfileView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', UserRegistrationView.as_view(), name='create'),
    path('login/', UserLogInView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password')
]