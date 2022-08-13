from django.urls import path
from .views import home, profile, RegisterView

urlpatterns = [
    path('', home, name='index'),
    path('profile/', profile, name='users-profile'),
]
