import os
from django.urls import path
from . import views
# from configrate.views import UserDataJson,RegisterView
# from django.contrib.auth import views as auth_views #new
urlpatterns = [
path('store/', views.store_item.as_view(), name='store'),
path('storeJson/', views.storeJson.as_view(), name='storeJson'),
    
]
