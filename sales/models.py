from django.db import models
from parent.models import  BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator,RegexValidator 
from django.db import transaction, IntegrityError

# from decimal import *
import datetime
from django.core.exceptions import ObjectDoesNotExist, FieldError,MultipleObjectsReturned
from django.db import models
from django.db.models import F, Sum, FloatField, Q
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import F
from configrate.models import Unit,Store
from input.models import Items
from parent.models import  BaseModel
import traceback


# Create your models here.
class Customer(BaseModel):
    name_lo = models.CharField("الاسم المحلي",max_length=50)
    name_fk = models.CharField("الاسم الاجنبي",max_length=50)
    phone   = models.CharField("رقم الجوال",max_length=50,blank=True,null=True)
    is_stop = models.BooleanField(default=True)
    def __str__(self):
        return self.name_lo

class SalesOperation(BaseModel):
    code = models.CharField(max_length=50)
    date = models.DateField(verbose_name="date")
    is_stage = models.BooleanField(verbose_name="is stage", default=False)
    is_suspended = models.BooleanField(verbose_name="is suspended", default=False)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        verbose_name="Customer", 
    )
    tax = models.FloatField(verbose_name="tax", blank=True, null=True)
    due_date = models.DateField(verbose_name="due date", null=True, blank=True)
    check_amount = models.FloatField("Check Amount", null=True, blank=True)
    stop = models.BooleanField("Stop", default=False)
    amount = models.FloatField("Total Amount For Invoicelocal",null=True,blank=True)
    statement = models.CharField(verbose_name="Statement", max_length=100)
    reference_number = models.CharField(
        verbose_name="Reference Number", max_length=100, null=True, blank=True
    )
    total_amount = models.FloatField("Total Amount")
    discount = models.FloatField("Discount", default=0)
    discount_rate = models.FloatField("discount rate %", null=True, blank=True)
    
    def __str__(self):
        return str(self.code)

    class Meta:
        abstract = True


class SalesOperationDetails(BaseModel):
    item = models.ForeignKey(Items, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(verbose_name="qty")
    free_qty = models.PositiveIntegerField(verbose_name="free qty", default=0)
    # expire_date = models.CharField(verbose_name="expire date",max_length=50)
    statement = models.CharField(
        verbose_name="Statement", max_length=100, null=True, blank=True
    )
    discount = models.FloatField("Discount", null=True, blank=True, default=0)
    discount_rate = models.FloatField("discount %", null=True, blank=True)
    store = models.ForeignKey(
        Store, on_delete=models.PROTECT, null=True, blank=True
    )
    def __str__(self):
        return str(self.item)
    class Meta:
        abstract = True


class SalesInvoicelocal(SalesOperation):
    class Meta:
        db_table = "Sales_invoicelocal"
        verbose_name = "Sales Invoice local"


class SalesInvoicelocalDetails(SalesOperationDetails):
  
    selling_price = models.FloatField("Selling price", null=True, blank=True)
    Sales_invoicelocal = models.ForeignKey(
        SalesInvoicelocal, on_delete=models.CASCADE
    )
    class Meta:
        db_table = "Sales_invoicelocal_details"
        verbose_name = "Sales invoicelocal details"




   
