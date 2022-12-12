

import os
from django.urls import path, include

from django.contrib.auth import views as auth_views #new
urlpatterns = [
path('', include('input.Category.urls')),
path('', include('input.Items.urls')),
]
 