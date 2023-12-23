from django.urls import path,include
from sales import views
from django.conf.urls import url


urlpatterns = [
     path('', include('sales.Customer.urls')), 
    path('SalesListJson/', views.SalesListJson.as_view(),name="SalesListJson"),
     path('SalesInvoice', views.SalesInvoice.as_view(),name='SalesInvoice'),
     path('get_code_SalesInvoice/', views.get_code, name='get_code_SalesInvoice'),
     path("get_store_items/",views.get_store_items, name='get_store_items'),
     path("get_store_items_data/",views.get_store_items_data, name='get_store_items_data'),
]    
