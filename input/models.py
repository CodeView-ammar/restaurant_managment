from django.db import models
from configrate.models import Unit,Items_type,Store
from parent.models import  BaseModel
    
class Category(BaseModel):
    name_lo =models.CharField("الاسم المحلي",max_length=50)
    name_fk  =models.CharField("الاسم الاجنبي",max_length=50)
    is_stop=models.BooleanField(default=True)
    def __str__(self):
        return self.name_lo
class Items(BaseModel):
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE)
    items_type=models.ForeignKey(Items_type,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    barcode=models.CharField("باركود",max_length=50)
    name_lo=models.CharField("اسم الصنف المحلي",max_length=50,unique=True)
    name_fk=models.CharField("اسم الصنف الاجنبي",max_length=50,default="")
    image = models.ImageField("صورة المنتج",upload_to="item",default="default.jpg")
    purch_price= models.CharField("Purchased Price",max_length=100)
    salse_price= models.CharField("Salse Price",max_length=100)
    
    def __str__(self):
        return self.name_lo

class story_items(BaseModel):
    qty=models.IntegerField("الكمية")
    Items=models.ForeignKey(Items,on_delete=models.CASCADE)
    stor=models.ForeignKey(Store,on_delete=models.CASCADE,null=True,blank=True)
    # exp_date=models.CharField("تاريخ الإنتهاء ")
    selling_price = models.FloatField("Selling price")
    purch_price = models.FloatField("purchases price")

