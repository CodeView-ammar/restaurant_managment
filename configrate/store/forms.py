from django import forms
from configrate.models import Store

class storeForm(forms.ModelForm):
    class Meta:
        model=Store
        fields="__all__"

