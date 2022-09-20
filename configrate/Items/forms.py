from django import forms
from configrate.models import Items

class ItemsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemsForm, self).__init__(*args, **kwargs)
        self.fields['unit'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['items_type'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['barcode'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['name_lo'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['name_fk'].widget.attrs.update({
            'class': 'formset-field  form-control'})




    
    class Meta:
        model=Items
        fields="__all__"

