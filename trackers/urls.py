from django.urls import path
from . import views, api

app_name = 'trackers'

urlpatterns = [
    # Dashboard
    path('dashboard/<int:pet_id>/', views.tracker_dashboard, name='tracker_dashboard'),
    
    # API Endpoints
    path('api/<int:pet_id>/update_location/', api.update_location, name='api_update_location'),
    path('api/<int:pet_id>/history/', api.get_location_history, name='api_location_history'),
    path('api/<int:pet_id>/alerts/', api.get_alerts, name='api_get_alerts'),
    path('api/<int:pet_id>/alerts/clear/', api.clear_alerts, name='api_clear_alerts'),
    path('api/<int:pet_id>/geofence/set/', api.set_geofence, name='api_set_geofence'),
    path('api/<int:pet_id>/geofence/get/', api.get_geofence, name='api_get_geofence'),
]
