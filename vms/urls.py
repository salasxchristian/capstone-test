from django.urls import path
from .views import *

app_name = 'vms'

urlpatterns = [
    path('checkin/', VMSCheckInCreateView.as_view(), name='checkin'), #reviewed
    path('settings/', VMSAdminView.as_view(), name='settings'), 
    path('kiosk/checkin/', VMSKioskCheckInCreateView.as_view(), name='kiosk_checkin'), #reviewed
    path('api/kiosk/<int:id>/token', VMSKioskTokenRetrieveAPIView.as_view(), name='api_kiosk_token'),
    path('kiosk/location/create/', VMSKioskLocationCreateView.as_view(), name='kiosk_location_create'),
    path('kiosk/location/<int:pk>/edit', VMSKioskLocationEditView.as_view(), name='kiosk_location_edit'),
    path('kiosk/location/<int:pk>/delete', VMSKioskLocationDeleteView.as_view(), name='kiosk_location_delete'),
    path('kiosk/token/create/', VMSKioskTokenCreateView.as_view(), name='kiosk_token_create'),
    path('kiosk/token/<int:pk>/edit', VMSKioskTokenEditView.as_view(), name='kiosk_token_edit'),
    path('kiosk/token/<int:pk>/delete', VMSKioskTokenDeleteView.as_view(), name='kiosk_token_delete'),
    path('kiosk/org/create/', VMSOrganizationCreateView.as_view(), name='kiosk_org_create'),
    path('kiosk/org/<int:pk>/edit', VMSOrganizationUpdateView.as_view(), name='kiosk_org_edit'),
    path('kiosk/org/<int:pk>/delete', VMSOrganizationDeleteView.as_view(), name='kiosk_org_delete'),
    path('history/', VMSCheckInHistoryView.as_view(), name='checkin_history'),
    path('history/active/', ActiveVMSCheckInView.as_view(), name='checkin_active'), #
    path('checkout/<int:pk>/', VMSCheckOut.as_view(), name='checkout'),
]