import os
from django.urls import path
from . import views
# from configrate.views import UserDataJson,RegisterView
# from django.contrib.auth import views as auth_views #new
urlpatterns = [
path('category/', views.Category_view.as_view(), name='Category'),
path('categoryJson/', views.CategoryJson.as_view(), name='CategoryJson'),
    
]
