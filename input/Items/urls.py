import os
from django.urls import path
from . import views
# from configrate.views import UserDataJson,RegisterView
# from django.contrib.auth import views as auth_views #new
urlpatterns = [
path('Items/', views.Items_item.as_view(), name='Items'),
path('ItemsJson/', views.ItemsJson.as_view(), name='ItemsJson'),
    
]
