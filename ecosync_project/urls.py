# ecosync_project/urls.py
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, include


admin.site.site_header = 'EcoSync Administration'
admin.site.index_title = 'Navigation'
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view(url='http://127.0.0.1:5173/dashboard')),
    path('auth/', include('core.urls')),
    path('', include('user_management.urls')),
    path('', include('profile_management.urls')),
    path('', include('rbac.urls')),
    path('', include('custom_api.urls')),
    path('', include('waste_management.urls')),
    path('', include('data_entry.urls')),
    path('', include('contractor.urls')),
    path('', include('managers.urls')),
    path('app/', include('citizen_engagement.urls')),
]
