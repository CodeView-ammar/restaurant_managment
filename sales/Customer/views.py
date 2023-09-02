from django.shortcuts import render
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.views.generic.edit import CreateView
from django.http import  JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views #new
from django.views import View

from sales.models import Customer
from .forms import CustomerForm

from django.core import serializers
from django.shortcuts import get_object_or_404
from django.http import QueryDict

class Customer_view(CreateView):

    def get(self, request, *args, **kwargs):
        if 'id' in request.GET.keys():
            if request.GET.get('id'):
                data=Customer.objects.filter(pk=request.GET.get('id'))
                
                
  
                result={'status':1,'data':serializers.serialize('json',data)}
            else:
                result={'status':0,'data':''}
            return JsonResponse(result)
        else:
        
            Uni=Customer.objects.all()
            fileduse=CustomerForm()
            context={
                "Items":Uni,
                "filed":fileduse
            }
    
        return render(request, 'sales/customer/customer.html',context)

    def post(self, request, *args, **kwargs):
        form = CustomerForm(request.POST)
        if request.POST.get('id'):
            data=get_object_or_404(Customer,pk=int(request.POST.get('id')))
            form=CustomerForm(request.POST,instance=data)
        item=[]
        if form.is_valid():
            item = form.save()
            item.save() # save in table 
            if request.POST.get('id'):
                if item.id:
                    result={'status':1,'message':"تم التعديل"}
                else:
                    result={'status':2,'message':"هناك هطاء بالتعديل"}
            else:
                if item.id:
                    result={'status':1,'message':"تم الحفظ"}
                else:
                    result={'status':2,'message':"هناك خطاء الحفظ"}
        else:
            result={'status':0,'error':form.errors.as_json()}
        return JsonResponse(result)
          
    def delete(self, request,*args, **kwargs):
        pk=int(QueryDict(request.body).get('id'))
        if pk:
            try:
                data=get_object_or_404(Customer,pk=pk)
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


class CustomerJson(BaseDatatableView):
    # The model we're going to show
    model = Customer

    # define the columns that will be returned
    columns = [
        'id',
        "name_lo",
        "name_fk",
        "phone",
        "is_stop",
        "created",
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
        "phone",
        "is_stop",
        "created",
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
        if column == "action":
            return '<a class="edit_row" data-url="{3}" data-id="{0}" style="DISPLAY: -webkit-inline-box;"  data-toggle="tooltip" title="{1}"><i class="fa fa-edit"></i></a><a class="delete_row" data-url="{3}" data-id="{0}"  style="    DISPLAY: -webkit-inline-box;"     data-toggle="tooltip" title="{2}"><i class="fa fa-trash"></i></a>'.format(row.pk,"Edit","Delete",reverse("Customer"))
            
            
        else:
            # We want to render Items as a custom column
            return super(CustomerJson, self).render_column(row, column)

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

