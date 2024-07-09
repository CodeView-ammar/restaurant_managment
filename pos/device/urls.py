import os
from django.urls import path
from pos.device import views
urlpatterns = [
path('device/', views.DeviceView.as_view(), name='device'),
path('deviceJson/', views.DeviceJson.as_view(), name='deviceJson'),
    
]
