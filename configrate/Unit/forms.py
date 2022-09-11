from django import forms
from configrate.models import Unit

class UnitForm(forms.ModelForm):
    class Meta:
        model=Unit
        fields="__all__"

