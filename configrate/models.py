from django.db import models


    

class Unit(models.Model):
    name_lo =models.CharField("الاسم المحلي",max_length=50)
    name_fk  =models.CharField("الاسم الاجنبي",max_length=50)
    codeUnit=models.CharField("رمز الوحدة",max_length=50)
    
    def __str__(self):
        return self.name_lo
class Items_type(models.Model):
    name_lo =models.CharField("الاسم المحلي",max_length=50)
    name_fk  =models.CharField("الاسم الاجنبي",max_length=50)
    def __str__(self):
        return self.name_lo
class Store(models.Model):
    name_lo =models.CharField("الاسم المحلي",max_length=50)
    name_fk  =models.CharField("الاسم الاجنبي",max_length=50)
    is_stop=models.BooleanField(default=True)
    def __str__(self):
        return self.name_lo
