import os
from django.urls import path
from . import views
# from configrate.views import UserDataJson,RegisterView
# from django.contrib.auth import views as auth_views #new
urlpatterns = [
path('Itemstype/', views.items_type_item.as_view(), name='Itemstype'),
path('itemstypeJson/', views.items_typeJson.as_view(), name='itemstypeJson'),
    
]
