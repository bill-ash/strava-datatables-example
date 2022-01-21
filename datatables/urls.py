from django.urls import path 
from .views import index, strava_auth, strava_callback
app_name = 'datatables'

urlpatterns = [
    path('strava/auth/', strava_auth, name='strava_auth'),
    path('stravacallback/', strava_callback, name='strava_callback'), 
    path('', index, name='index'),
]
