import os
from django.urls import path, include
from django.contrib.auth import views as auth_views #new
from .views import Customer_view, CustomerJson
urlpatterns = [
path('Customer',Customer_view.as_view(),name='Customer'),
path('CustomerJson',CustomerJson.as_view(),name='CustomerJson'),
]
 