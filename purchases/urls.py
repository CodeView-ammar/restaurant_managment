from django.urls import path,include
from purchases import views
from django.conf.urls import url


urlpatterns = [
     path('PurchaseListJson/', views.PurchaseListJson.as_view(),name="PurchaseListJson"),
     path('', include('purchases.Supplier.urls')),
     path('PurchaseInvoice', views.PurchaseInvoice.as_view(),name='PurchaseInvoice'),
     path('get_code/', views.get_code, name='get_code'),


]
