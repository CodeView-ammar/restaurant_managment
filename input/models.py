from django.db import models
from configrate.models import Unit,Items_type,Store

    
class Category(models.Model):
    name_lo =models.CharField("الاسم المحلي",max_length=50)
    name_fk  =models.CharField("الاسم الاجنبي",max_length=50)
    is_stop=models.BooleanField(default=True)
    def __str__(self):
        return self.name_lo
class Items(models.Model):
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE)
    items_type=models.ForeignKey(Items_type,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    barcode=models.CharField("باركود",max_length=50)
    name_lo=models.CharField("اسم الصنف المحلي",max_length=50,unique=True)
    name_fk=models.CharField("اسم الصنف الاجنبي",max_length=50,default="")
    def __str__(self):
        return self.name_lo

class story_items(models.Model):
    qty=models.IntegerField("الكمية")
    Items=models.ForeignKey(Items,on_delete=models.CASCADE)
    stor=models.ForeignKey(Store,on_delete=models.CASCADE)
    date_in=models.IntegerField("تاريخ الاضافة")


