import traceback
from django.shortcuts import render
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.views.generic.edit import CreateView
from django.http import  JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views #new
from django.views import View
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.http import QueryDict
from purchases.models import Purchases,PurchasesDetails
from purchases.forms import PurchasesForm,PurchasesDetailsForm
from django.forms import formset_factory,modelformset_factory
from django.db.models import Max
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

class PurchaseInvoicelocals(CreateView):
 
    
    def get(self, request, *args, **kwargs):
        """Function For get  Record and render record
        """

        result = {"status": 0, "message": ""}
        if "id" in request.GET.keys():

            if request.GET.get("id"):
                formdata = Purchases.objects.filter(
                    pk=int(request.GET.get("id"))
                )
         

                formsetdata = PurchasesDetails.objects.filter(
                    purchases_id=int(request.GET.get("id"))
                )

               

                result = {
                    "status": 1,
                    "data1": serializers.serialize("json", formdata),
                    "data2": serializers.serialize("json", formsetdata),
                }

             
                return JsonResponse(result)

        else:
            try:
             
                DataFormset = modelformset_factory(
                    PurchasesDetails, form=PurchasesDetailsForm
                )
                formset = DataFormset(
                    request.GET or None,
                    queryset=PurchasesDetails.objects.none(),
                    prefix="PurchasesDetails",
                )
                form1 = PurchasesForm()

                context = {
                    "form": form1,
                    "formset": formset,
                    "url": reverse("purchases"),
                    "title_list": "شاشة المشتريات المحلية",
                    }
            except ObjectDoesNotExist as e:

                data = "خطاء في جلب البيانات يجب عليك مراجعة المطور"
                context = {
                    "error": data,
                }
            return render(request, "purchases/purchases/purchases.html", context)

    def post(self, request, *args, **kwargs):
        result = {"status": 0, 
        "class": "",
        "message": ""}
        form = PurchasesForm(request.POST)
        DataFormset = modelformset_factory(
            PurchasesDetails, form=PurchasesDetailsForm
        )
        formset = DataFormset(
            request.POST or None,
            queryset=PurchasesDetails.objects.none(),
            prefix="PurchasesDetails",
        )

        if form.is_valid() and formset.is_valid():


            try:
               
                obj = form.save(commit=False)
                obj.save()
                if formset.is_valid():
                    details_obj = formset.save(commit=False)

                    for instance in details_obj:

                        instance.purchases_id = obj.id
                        instance.save()
                
                
                if request.POST.get("id_invoice"):
                    msg = "تم التعديل بنجاح"
                    result = {"status": 1, "message": msg}
                else:
                    msg = "تم الحفظ بنجاح"
                    result = {"status": 1, "message": msg}
            except IntegrityError as e:

                traceback.print_exc()

                result["status"] = 3
                result["message"] = {
                    "message": str(e),
                    "class": "alert alert-danger",
                }
                return JsonResponse(result)
            except ObjectDoesNotExist as e:
                traceback.print_exc()

                result = {"status": 3, "message": msg, "msg": "error"}

            except Exception as e:
                traceback.print_exc()
                msg = "inexcpacted error"
                result = {"status": 3, "message": msg, "msg": "error"}

        return JsonResponse(result)

    def delete(self, request, *args, **kwargs):
        result = {"status": 0, "message": ""}
        pk = int(QueryDict(request.body).get("id"))
        if pk:
            try:
                data = get_object_or_404(PurchaseInvoicelocal, pk=pk)

                data.delete()
                msg = message.delete_successfully()
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
                result = {"status": 3, "message": msg, "msg": "error"}
        else:
            msg = message.delete_error()
            result = {"status": 0, "message": msg}
        return JsonResponse(result)

def max_number(request):
    max_num=[]
    nax_num=Purchases.objects.aggregate(Max('number'))["number__max"]
    if nax_num:
        nax_num=int(nax_num)+1
    else:
        nax_num=1
    

    result={'status':1,"max_number":nax_num}
    return JsonResponse(result)

