from django.shortcuts import render

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.views.generic.edit import CreateView
from django.http import  JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views #new
from django.views import View

from ..models import Category
from ..models import Category
from .forms import CategoryForm

from django.urls import reverse
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.http import QueryDict

class Category_view(CreateView):

    def get(self, request, *args, **kwargs):
        if 'id' in request.GET.keys():
            if request.GET.get('id'):
                data=Category.objects.filter(pk=request.GET.get('id'))
                
                

                result={'status':1,'data':serializers.serialize('json',data)}
            else:
                result={'status':0,'data':''}
            return JsonResponse(result)
        else:
        
            Uni=Category.objects.all()
            fileduse=CategoryForm()
            context={
                "Category":Uni,
                "filed":fileduse
            }
        return render(request, 'Input/Category/category.html',context)


    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if request.POST.get('id'):
            data=get_object_or_404(Category,pk=int(request.POST.get('id')))
            form=CategoryForm(request.POST,instance=data)
        
        category=''
        if form.is_valid():
            category=form.save()


       

        if category.id:
            context={
                    "status":1,
                    "message":"تم الحفظ"
                }
        else:
            context={
                    "status":0,
                    "message":"خطاء في الحفظ"
                }
        return JsonResponse(context)
        
    def delete(self, request,*args, **kwargs):
        pk=int(QueryDict(request.body).get('id'))
        if pk:
            try:
                data=get_object_or_404(Category,pk=pk)
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


class CategoryJson(BaseDatatableView):
    # The model we're going to show
    model = Category

    # define the columns that will be returned
    columns = [
    'id',
    "name_lo",
    "name_fk",
    "is_stop",
    "action",
    ]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non-sortable columns use empty
    # value like ''
    order_columns = [
    'id',
    "name_lo",
    "name_fk",
    "is_stop",
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
        if column=="is_stop":
            if row.is_stop:
                return "مفعل"
            else:
                return "موقف"
        if column ==  "action":
            return '<a class="edit_row" data-url="{3}" data-id="{0}" style="DISPLAY: -webkit-inline-box;"  data-toggle="tooltip" title="{1}"><i class="fa fa-edit"></i></a><a class="delete_row" data-url="{3}" data-id="{0}"  style="    DISPLAY: -webkit-inline-box;"     data-toggle="tooltip" title="{2}"><i class="fa fa-trash"></i></a>'.format(row.pk,"Edit","Delete",reverse("Category"))
            
            
        else:
            # We want to render items_type as a custom column
            return super(CategoryJson, self).render_column(row, column)

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

