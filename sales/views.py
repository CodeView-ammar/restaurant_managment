import time
import os
import traceback
import datetime
import json


from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelformset_factory
from django.db.models import IntegerField
from django.db.models.functions import Cast



from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse,  HttpResponse, QueryDict
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.db import transaction, IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, CreateView, View, UpdateView, DeleteView
from django.urls import reverse
from django.db.models import Q, F
from django.conf import settings
from django.utils.html import format_html
from configrate.models import Unit,Store
from input.models import Items




from sales.forms import (
    SalesInvoiceForm,
    SalesInvoicelocalDetailsForm,
    
)
from sales.models import (
    SalesInvoicelocal,
    SalesInvoicelocalDetails,
)
from sales.Customer.forms import CustomerForm
from sales.models import  Customer

class SalesInvoice(CreateView):
    def get(self, request, *args, **kwargs):
        result = {"status": 0, "message": ""}

        if "id" in request.GET.keys():
            if request.GET.get("id"):
                formdata = SalesInvoicelocal.objects.filter(
                    pk=int(request.GET.get("id"))
                )
                customerdata1 = Customer.objects.values("id", "name_lo").get(
                    pk=formdata.values("customer")[0]['customer']
                )
                customerdata = {
                    "id": customerdata1["id"],
                    "name": customerdata1["name_lo"],
                }

                formsetdata = SalesInvoicelocalDetails.objects.filter(
                    Sales_invoicelocal_id=int(request.GET.get("id"))
                )

                listdata = []

                for i in formsetdata:
                    d = Items.objects.values("id", "name_lo", "name_fk").get(
                        pk=i.item_id
                    )
                    listdata.append(d)

                # data_item =

                result = {
                    "status": 1,
                    "datacustomer": customerdata,
                    "dataitem": listdata,
                    "data1": serializers.serialize("json", formdata),
                    "data2": serializers.serialize("json", formsetdata,fields=("item","unit","qty","selling_price","expire_date","discount","store")),
                }

                # except:
                # result={'status':0,'data':"not found"}

                return JsonResponse(result)

        else:
  
            try:

                DataFormset = modelformset_factory(
                    SalesInvoicelocalDetails, form=SalesInvoicelocalDetailsForm
                )
                formset = DataFormset(
                    request.GET or None,
                    queryset=SalesInvoicelocalDetails.objects.none(),
                    prefix="SalesInvoicelocalDetails",
                )
                db_years_name=0
                

                form1 = SalesInvoiceForm()

                context = {
                    "Variable":{
                        "is_expire_date":1
                        },
                    "form": form1,
                    "formset": formset,
                    "url": reverse("SalesInvoice"),
                    "title_list": _("Sales Invoice local"),
                    "dialog_form1": CustomerForm(),
                    "dialog_form_title1": _("Add Customer "),
                    "dialog_form_title2": _("Add Store "),
                }
            except ObjectDoesNotExist as e:

                data = _("Error must initial GeneralVariables in app customer")

                result = {
                    "status": 0,
                    "message": {"message": data, "class": "alert alert-danger"},
                }
                # return JsonResponse(result)
                context = {
                    "error": data,
                }
                
            return render(request, "sales/sales_invoice/sales_invoice.html", context)

    def post(self, request, *args, **kwargs):
        result = {"status": 0, "class": "","message": ""}
        is_note=None
        is_expire_date = None    
        db_years_name=0
        db_years_name=2023
        Variable={
                "is_note":is_note,
                'is_expire_date':is_expire_date,
                "years_date":db_years_name,

            }
        form = SalesInvoiceForm(request.POST)
        DataFormset = modelformset_factory(
            SalesInvoicelocalDetails, form=SalesInvoicelocalDetailsForm
        )
        formset = DataFormset(
            request.POST or None,
            queryset=SalesInvoicelocalDetails.objects.none(),
            prefix="SalesInvoicelocalDetails",
        )

        result = {"status": 0, "message": "aaaa"}
        if request.POST.get("id_sales_invo"):
            
            try:
                id_sales_invo = int(request.POST["id_sales_invo"])
                data_form = get_object_or_404(
                    SalesInvoicelocal, pk=int(request.POST["id_sales_invo"])
                )
                obj_edit = SalesInvoicelocal.objects.get(pk=id_sales_invo)

       
                form = SalesInvoiceForm(request.POST, instance=data_form)

                formset = DataFormset(
                    request.POST,
                    queryset=SalesInvoicelocalDetails.objects.none(),
                    prefix="SalesInvoicelocalDetails",
                )
                
            except Exception as e:
                traceback.print_exc()

                msg = "error"
                result = {"status": 3, "message": msg}
                return JsonResponse(result)



        if form.is_valid() and formset.is_valid():

            try:
               
                obj = form.save(commit=False)
                if request.POST.get("id_sales_invo"):
                    obj.modified_by_id = request.user.id
                    SalesInvoicelocalDetails.objects.filter(sales_invoicelocal_id = obj.id).delete()
                else:
                    obj.created_by_id = request.user.id
                
                if not request.POST.get("id_sales_invo"):
                    obj.code = get_maxcode()
                obj.save()
                if formset.is_valid():
                    details_obj = formset.save(commit=False)
                    
                    qty=0
                    for instance in details_obj:
                        instance.Sales_invoicelocal_id = obj.id
                        instance.store_id=request.POST.get("store")
                        qoty = story_items.objects.filter(Items_id=instance.item, stor_id=instance.store).first()
                        if qoty:
                            qoty.qty = int(qoty.qty) - int(instance.qty)
                            qoty.save()
                        else:
                            result = {"status": 3, "message": "الكمية غير متوفرة بالمخزن", "msg": "error"}
                            return JsonResponse(result)

                        instance.save()
                doc_id = 0
                if request.POST.get("id_sales_invo"):
                    msg = "تم التعديل بنجاح"
                    result = {"status": 1, "message": msg}
                else:
                    msg = "تم الحفظ بنجاح"
                    result = {"status": 1, "message": msg}
            except ObjectDoesNotExist as e:
                traceback.print_exc()
                msg = str(e)
                result = {"status": 3, "message": msg, "msg": "error"}

            except Exception as e:
                traceback.print_exc()
                msg = "inexcpacted error"
                result = {"status": 3, "message": msg, "msg": "error"}

        else:
            if not formset.is_valid():

                row = 0
                for f in formset.forms:
                    if not f.is_valid():
                        result = {
                            "status": 0,
                            "error": "",
                            "error2": f.errors.as_json(),
                            "row": row,
                        }
                        break
                    row = row + 1

            else:                
                result = {"status": 0, "error": form.errors}

        return JsonResponse(result)

    def delete(self, request, *args, **kwargs):
        result = {"status": 0, "message": ""}
        pk = int(QueryDict(request.body).get("id"))
        if pk:
            try:
                data = get_object_or_404(SalesInvoicelocal, pk=pk)

                data.delete()
                msg = "تم الحذف بنجاح"
                result = {"status": 1, "message": msg}
            except InvoiceExcept as e:
                result["status"] = 3
                result["message"] = {
                    "message": str(e),
                    "class": "alert alert-danger",
                }
                return JsonResponse(result)
            except Exception as e:
                msg = str(e)
                result = {"status": 3, "message": msg, "msg": _("error")}
        else:
            msg = "خطاء بالحذف"
            result = {"status": 0, "message": msg}
        return JsonResponse(result)


def get_code(request):
  
    new_code = get_maxcode()
    data = {"status": 1, "data": new_code}
    return JsonResponse(data)
from input.models import story_items
from django.core import serializers


def get_store_items(request):
    id_item=request.GET.get("id_item")
    id_store=request.GET.get("id_store")
    if(id_item):
        data_=story_items.objects.filter(stor_id=int(id_store),Items_id=int(id_item))
        result = {"status": 1, "data": data_}
    else:
        result = {"status":0, "data": ""}
    return JsonResponse(result)


def get_store_items_data(request):
    id_item=request.GET.get("id_item")
    id_store=request.GET.get("id_store")
    expire_date=request.GET.get("expire_date")
    if(id_item):

        data_=story_items.objects.filter(stor=id_store,Items=id_item)
        result = {"status": 1, "data": serializers.serialize("json", data_)}
    else:
        result = {"status":0, "data": ""}
    return JsonResponse(result)




def get_maxcode():
    
    code=SalesInvoicelocal.objects.all().annotate(code1=Cast(F('code'),output_field=IntegerField())).aggregate(id_max=Max((("code1")),output_field=IntegerField()))
    
    number_max = next(iter(code.values()))
    if number_max != None:
        new_code = int(number_max) + 1
    else:
        new_code = "1"
    return new_code


class SalesListJson(BaseDatatableView):
    model = SalesInvoicelocal
    columns = [
        
        "code",
        "date",
        "supplir__name_lo",
        "total_amount",
        "action"
    ]

    order_columns = [
        "code",
        "date",
        "customer__name_lo",
        "total_amount",
        "action",
    ]

    def get_initial_queryset(self):
        return self.model.objects.values(
            "id",
            "code",
            "date",
            "customer__name_lo",
            "total_amount",
        ).filter(stop=False)

    count = 0

    def render_column(self, row, column):
        if column == "#":
            self.count += 1
            return str(self.count)
        elif column == "action":
            return '<a class="edit_row" data-url="{3}" data-id="{0}" style="DISPLAY: ' \
                   '-webkit-inline-box;margin-right:5px;"  data-toggle="tooltip" title="{1}"><i class="fa ' \
                   'fa-edit"></i></a><a class="delete_row" data-url="{3}" data-id="{0}"  style="DISPLAY: ' \
                   '-webkit-inline-box;margin-right:5px;" data-toggle="tooltip" title="{2}"><i class="fa ' \
                   'fa-trash"></i></a>'.format(
                row['id'], _("تعديل"), _("حذف"), reverse("SalesInvoice"))
        else:
            return super(SalesListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        """To Filter data in table using in search
        """
        sSearch = self.request.GET.get("sSearch", None)
        if sSearch:
            qs = qs.filter(
                Q(id__icontains=sSearch)
                | Q(code__icontains=sSearch)
            )
        return qs
