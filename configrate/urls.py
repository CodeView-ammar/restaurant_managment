

import os
from django.urls import path, include

from configrate.views import UserDataJson,RegisterView
from django.contrib.auth import views as auth_views #new
urlpatterns = [
# path('usersview',get_users.as_view(),name='usersview'),
path('register/', RegisterView.as_view(), name='users-register'),
path('UserDataJson', UserDataJson.as_view(), name='UserDataJson'),
path('', include('configrate.Unit.urls')),
path('', include('configrate.itemtype.urls')),
path('', include('configrate.store.urls')),

]
