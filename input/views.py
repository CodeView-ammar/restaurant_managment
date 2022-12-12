from django.shortcuts import render

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from .forms import UserForm
from django.views.generic.edit import CreateView
from django.http import  JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views #new
from django.views import View
from .forms import RegisterForm
from django.urls import reverse
from django.core import serializers

from django.shortcuts import get_object_or_404
from django.http import QueryDict


 