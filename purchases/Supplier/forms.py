from django import forms
from purchases.models import Supplier

class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        self.fields['name_lo'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['name_fk'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['phone'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['is_stop'].widget.attrs.update({
            'class': 'formset-field  form-control'})
      

    
    class Meta:
        model=Supplier
        fields="__all__"
        execute="created"

