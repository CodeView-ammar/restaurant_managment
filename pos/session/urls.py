import os
from django.urls import path
from pos.session import views
urlpatterns = [
path('session/', views.SessionView.as_view(), name='session'),
path('edet-status/', views.edit_status, name='edit_status'),
path('sessionJson/', views.SessionJson.as_view(), name='sessionJson'),
    
]
