from django import forms
from configrate.models import Items_type

class items_typeForm(forms.ModelForm):
    class Meta:
        model=Items_type
        fields="__all__"

