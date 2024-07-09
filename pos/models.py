from django.db import models
from parent.models import BaseModel
from sales.models import Customer

# Create your models here.
class Setting(BaseModel):
    def_customer= models.ForeignKey(Customer,on_delete=models.CASCADE)



class Device(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name+""


class Session(BaseModel):
    STATUS_CHOICES={
        ("open","open"),
        ("closed","closed"),
    }
    device= models.ForeignKey(Device, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default="open",null=True, blank=True)



