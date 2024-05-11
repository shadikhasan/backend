# urls.py
from django.urls import path, include
from . import views
from core.views import *
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'public-notifications', PublicNotificationViewSet)


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', UserLogInView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    
    #report issue
    path('issue-reports/create/', IssueReportCreateView.as_view(), name='issue-report-create'),
    path('volunteer-registration/', VolunteerRegistrationCreateAPIView.as_view(), name='volunteer-registration-create'),
    
    
    path('', include(router.urls)),
]
