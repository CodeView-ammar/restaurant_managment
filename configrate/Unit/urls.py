import os
from django.urls import path
from . import views
# from configrate.views import UserDataJson,RegisterView
# from django.contrib.auth import views as auth_views #new
urlpatterns = [
path('unit/', views.unit_item.as_view(), name='unit'),
path('UnitJson/', views.UnitJson.as_view(), name='UnitJson'),
    
]
