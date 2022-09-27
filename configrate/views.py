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
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'configrate/users.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        # if request.user.is_authenticated:
        #     return redirect(to')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        
        if 'id' in request.GET.keys():
            if request.GET.get('id'):
                data=User.objects.filter(pk=request.GET.get('id'))
                
                

                result={'status':1,'data':serializers.serialize('json',data)}
            else:
                result={'status':0,'data':''}
            return JsonResponse(result)
        else:
            form = RegisterForm()
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if request.POST.get('id'):
            data=get_object_or_404(User,pk=int(request.POST.get('id')))
            form=RegisterForm(request.POST,instance=data)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            context={
                    "status":1,
                    "message":"تم الحفظ"
                }
        else:
            context={
                "status":0,
                "message":form.errors
            }
    
        return JsonResponse(context)

    def delete(self, request,*args, **kwargs):
        pk=int(QueryDict(request.body).get('id'))
        if pk:
            try:
                data=get_object_or_404(User,pk=pk)
                data.delete()
                msg="تم الحذف"
                result={'status':1,'message':msg}
            except:
                msg="خطاء بالحذف"
                result={'status':0,'message':msg}
        else:
            msg="لا يوجد الصنف"
            result={'status':0,'message':msg}
        return JsonResponse(result)

# def get_users(request):
#     user=UserR.objects.all()
#     fileduse=UserForm()
#     context={
#         "user":user,
#         "filed":fileduse
#     }
    
#     return render(request, 'configrate/users.html',context)


class UserDataJson(BaseDatatableView):
    # The model we're going to show
    model = User

    # define the columns that will be returned
    columns = [
    'id',
    "first_name",
    "last_name",
    "username",
     "action",
    ]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non-sortable columns use empty
    # value like ''
    order_columns = [
    'id',
    "first_name",
    "last_name",
    "username",
    "action",
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500
    count = 0
    def render_column(self, row, column):
        if column == "id":
            self.count += 1
            return self.count
        if column ==  "action":
             return '<a class="edit_row" data-url="{3}" data-id="{0}" style="DISPLAY: -webkit-inline-box;"  data-toggle="tooltip" title="{1}"><i class="fa fa-edit"></i></a><a class="delete_row" data-url="{3}" data-id="{0}"  style="    DISPLAY: -webkit-inline-box;"     data-toggle="tooltip" title="{2}"><i class="fa fa-trash"></i></a>'.format(row.pk,"تعديل","حذف",reverse("users-register"))
        else:
            # We want to render user as a custom column
            return super(UserDataJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name__istartswith=search)

        # more advanced example using extra parameters
        filter_customer = self.request.GET.get('customer', None)

        if filter_customer:
            customer_parts = filter_customer.split(' ')
            qs_params = None
            for part in customer_parts:
                q = Q(customer_firstname__istartswith=part) | Q(customer_lastname__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

