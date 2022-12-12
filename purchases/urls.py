import os
from django.urls import path, include
from django.contrib.auth import views as auth_views #new
from purchases.views import PurchaseInvoicelocals,max_number
urlpatterns = [
path('', include('purchases.Supplier.urls')),
path('purchases', PurchaseInvoicelocals.as_view(),name='purchases'),
path('max_number', max_number,name='max_number'),
]
 