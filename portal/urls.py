from django.urls import path
from django.views.generic import RedirectView
from .views import * 

app_name = 'portal'

urlpatterns = [
    path('', RedirectView.as_view(url='/landing'), name='home'),
    path('landing/', LandingPageView.as_view(), name='landing'),
    path('admin/settings/', SettingsAdminView.as_view(), name='admin_settings'),
]