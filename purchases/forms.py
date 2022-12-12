from django import forms
from purchases.models import Purchases,PurchasesDetails,Supplier
from datetime import timedelta
from datetime import date
from input.models import Store,Items
class PurchasesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PurchasesForm, self).__init__(*args, **kwargs)
        self.fields["number"] = forms.CharField(
            required=True,
            label='الرقم',
            widget=forms.TextInput(
                attrs={
                    "readonly": "readonly",
                    "class": "form-field number number_id form-control",
                }
            ),
        )
        self.fields["date"] = forms.DateField(
            required=False,
            initial=date.today(),
            label="التاريخ",
            widget=forms.DateInput(
                attrs={"type": "date","class":"form-control", "required": True}
            ),
        )
         
        self.fields["notes"] = forms.CharField(
            required=False,
            label='البيان',
            widget=forms.Textarea(attrs={"rows": "2", "column": "1","class": "form-field form-control"}))

        self.fields["amount"] = forms.DecimalField(
            label="الإجمالي",
            max_digits=12,
            decimal_places=2,
            widget=forms.NumberInput(attrs={"min": "0", "step": "1","readonly":"readonly","class":"form-control"}),
        )
        self.fields["supplir"] = forms.ModelChoiceField(
            queryset=Supplier.objects.all(),
            label='المورد',
        )
        self.fields["store"] = forms.ModelChoiceField(
            queryset=Store.objects.all(),
            label='المخزن',
        )
       
        self.fields["supplir"].widget.attrs.update({"class":"form-control"})
        self.fields["store"].widget.attrs.update({"class":"form-control"})



    class Meta:
        model=Purchases
        
        fields="__all__"

class PurchasesDetailsForm(forms.ModelForm):
    
    total=forms.CharField(max_length=50,
        label='store',
    )
    def __init__(self, *args, **kwargs):
        try:
            
            row = next(kwargs.pop("row"))
        except:
            row = None
        super(PurchasesDetailsForm, self).__init__(*args, **kwargs)

        self.fields["purchases"]=forms.IntegerField(required=False)
        self.fields["items"] = forms.ModelChoiceField(
            queryset=Items.objects.all(),
            label='الصنف',
        )
        

        self.fields["items"].widget.attrs.update({"class":"form-control formset-field"})
        self.fields["price"].widget.attrs.update({"class":"form-control formset-field "})
        self.fields["qty"].widget.attrs.update({"class":"form-control formset-field"
        ,"onchange": "getTotalItem(this)",
        })
        self.fields["total"].widget.attrs.update({"class":"form-control total_items formset-field","readonly":"readonly"})
        self.fields["date_end"] = forms.DateField(
            required=False,
            initial=date.today(),
            label="تاريخ الإنتهاء",
            widget=forms.DateInput(
                attrs={"type": "date", "class":"formset-field", "required": True}
            ),
        )
        
    class Meta:
        model=PurchasesDetails
        fields=[
            "purchases",
            "items",
            "price",
            "qty",
            "date_end",
        ]