from django.db import models
from parent.models import BaseModel
from sales.models import Customer

# Create your models here.
class Setting(BaseModel):
    def_customer= models.ForeignKey(Customer,on_delete=models.CASCADE)



class Device(BaseModel):
    name = models.CharField(max_length=100)



class Session(BaseModel):
    Device= models.ForeignKey(Device, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)




