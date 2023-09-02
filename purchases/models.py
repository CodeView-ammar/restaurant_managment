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
class Supplier(BaseModel):
    name_lo = models.CharField("الاسم المحلي",max_length=50)
    name_fk = models.CharField("الاسم الاجنبي",max_length=50)
    phone   = models.CharField("رقم الجوال",max_length=50,blank=True,null=True)
    is_stop = models.BooleanField(default=True)
    def __str__(self):
        return self.name_lo




class PurchaseOperation(BaseModel):
    code = models.CharField(max_length=50)
    date = models.DateField(verbose_name=_("date"))
    is_stage = models.BooleanField(verbose_name=_("is stage"), default=False)
    is_suspended = models.BooleanField(verbose_name=_("is suspended"), default=False)
    supplir = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        verbose_name=_("supplier"), 
    )
    tax = models.FloatField(verbose_name=_("tax"), blank=True, null=True)
    due_date = models.DateField(verbose_name=_("due date"), null=True, blank=True)
    check_amount = models.FloatField(_("Check Amount"), null=True, blank=True)
    supplier_bill_number = models.IntegerField(
        verbose_name=_("Supplier Bill Number"), null=True, blank=True
    )
    supplier_bill_date = models.DateField(
        verbose_name=_("Supplier Bill Date"), null=True, blank=True
    )
    stop = models.BooleanField(_("Stop"), default=False)
    amount = models.FloatField(_("Total Amount For Invoicelocal"),null=True,blank=True)
    statement = models.CharField(verbose_name=_("Statement"), max_length=100)
    reference_number = models.CharField(
        verbose_name=_("Reference Number"), max_length=100, null=True, blank=True
    )
    total_amount = models.FloatField(_("Total Amount"))
    discount = models.FloatField(_("Discount"), default=0)
    discount_rate = models.FloatField(_("discount rate %"), null=True, blank=True)
    
    def __str__(self):
        return str(self.code)

    class Meta:
        abstract = True


class PurchaseOperationDetails(BaseModel):
    item = models.ForeignKey(Items, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(verbose_name=_("qty"))
    free_qty = models.PositiveIntegerField(verbose_name=_("free qty"), default=0)
    price = models.DecimalField(verbose_name=_("price"), max_digits=8, decimal_places=2)
    expire_date = models.DateField(verbose_name=_("expire date"), null=True, blank=True)
    statement = models.CharField(
        verbose_name=_("Statement"), max_length=100, null=True, blank=True
    )
    discount = models.FloatField(_("Discount"), null=True, blank=True, default=0)
    discount_rate = models.FloatField(_("discount %"), null=True, blank=True)
    store = models.ForeignKey(
        Store, on_delete=models.PROTECT, null=True, blank=True
    )
    def __str__(self):
        return str(self.item)
    class Meta:
        abstract = True


class PurchaseInvoicelocal(PurchaseOperation):
    class Meta:
        db_table = "purchase_invoicelocal"
        verbose_name = _("Purchase Invoice local")


class PurchaseInvoicelocalDetails(PurchaseOperationDetails):
  
    selling_price = models.FloatField(_("Selling price"), null=True, blank=True)
    purchase_invoicelocal = models.ForeignKey(
        PurchaseInvoicelocal, on_delete=models.CASCADE
    )
    class Meta:
        db_table = "purchase_invoicelocal_details"
        verbose_name = _("purchase invoicelocal details")




   
