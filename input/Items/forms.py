from django import forms
from input.models import Items

class ItemsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemsForm, self).__init__(*args, **kwargs)
        self.fields['unit'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['category'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['items_type'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['barcode'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['name_lo'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['name_fk'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['image'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['salse_price'].widget.attrs.update({
            'class': 'formset-field  form-control'})
        self.fields['purch_price'].widget.attrs.update({
            'class': 'formset-field  form-control'})



    
    class Meta:
        model=Items
        fields="__all__"

