from django.urls import path,include
from pos import views
from django.conf.urls import url


urlpatterns = [
path("",include("pos.pos.urls")),
path("",include("pos.device.urls")),
path("",include("pos.session.urls")),
]
