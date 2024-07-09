from django import forms
from pos.models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model=Device
        fields="__all__"

