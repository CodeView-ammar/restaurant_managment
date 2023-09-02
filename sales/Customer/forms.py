from django import forms
from sales.models import Customer

class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['name_lo'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['name_fk'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['phone'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['is_stop'].widget.attrs.update({
            'class': 'formset-field  form-control'})
      

    
    class Meta:
        model=Customer
        fields="__all__"
        execute="created"

