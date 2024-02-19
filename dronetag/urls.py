from django.urls import path
from .views import *

urlpatterns = [
    path('', map_dashboard_view, name='map_dashboard_view'),
    path('link_reliability_dashboard/', link_reliability_dashboard, name='link_reliability_dashboard'),
    path('api/telemetry_messege/', TelemetryMessageAPI.as_view(), name='t_message'),
    path('api/status_messege/', StatusMessageAPI.as_view(), name='s_message')
]