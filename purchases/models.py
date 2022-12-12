from django.db import models
from input.models import Items,Store
# Create your models here.
class Supplier(models.Model):
    name_lo = models.CharField("الاسم المحلي",max_length=50)
    name_fk = models.CharField("الاسم الاجنبي",max_length=50)
    phone   = models.CharField("رقم الجوال",max_length=50,blank=True,null=True)
    is_stop = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name_lo


class Purchases(models.Model):
    number= models.IntegerField("رقم الفاتورة",null=False)
    date= models.DateField("التاريخ",null=False)
    notes= models.TextField("الملاحظة")
    supplir = models.ForeignKey(Supplier,on_delete=models.PROTECT,verbose_name="المورد"),
    amount = models.FloatField("الإجمالي",null=True,blank=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE,verbose_name="المخز")

class PurchasesDetails(models.Model):
    purchases= models.ForeignKey(Purchases, on_delete=models.CASCADE)
    items= models.ForeignKey(Items, on_delete=models.CASCADE,verbose_name="الصنف")
    price= models.FloatField("السعر",null=True)
    qty = models.IntegerField("الكمية",null=True)
    date_end = models.DateField("تاريخ الإنتهاء")    
    
    
    