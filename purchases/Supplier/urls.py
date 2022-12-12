import os
from django.urls import path, include
from django.contrib.auth import views as auth_views #new
from .views import Supplier_view, SupplierJson
urlpatterns = [
path('Supplier',Supplier_view.as_view(),name='supplier'),
path('SupplierJson',SupplierJson.as_view(),name='SupplierJson'),
]
 