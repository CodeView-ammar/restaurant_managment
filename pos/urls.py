from django.urls import path,include
from pos import views
from django.conf.urls import url


urlpatterns = [
path('pos/',views.pos_index,name="pos"),
]
