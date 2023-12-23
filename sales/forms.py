import datetime
from django import forms
from django.db import models

from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from django.core.exceptions import ObjectDoesNotExist
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, ButtonHolder, Div
from crispy_forms.bootstrap import InlineRadios, InlineField, FormActions

from sales.models import (SalesInvoicelocal,SalesInvoicelocalDetails,
)
from configrate.models import Unit,Store
from input.models import Items

from django.urls import reverse_lazy
from datetime import timedelta
from datetime import date
from sales.models import Customer




class SalesInvoiceForm(forms.ModelForm):
    store = forms.ModelChoiceField(
        queryset=Store.objects.all(),
        label=_('المخزن'),
    )

    def __init__(self, *args, **kwargs):
        super(SalesInvoiceForm, self).__init__(*args, **kwargs)
        
        
        
        self.fields["customer"] = forms.ModelChoiceField(
            label=_("العميل"),
            queryset=Customer.objects.all(),
            # widget=autocomplete.ModelSelect2(url="SupplirItemAutocomplete1",),
        )

        self.fields["discount_item"] = forms.FloatField(
            label=_("إجمالي خصم الاصناف"),
            required=False,
            widget=forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                    "value":0,
                    "placeholder": _("قيمة"),
                }
            ),
        )
      
        self.fields["total_net_bill"] = forms.FloatField(
            label=_("إجمالي بعد الخصم"),
            required=False,
            widget=forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                    "placeholder": _("قيمة"),
                }
            ),
        )

        self.fields["date"] = forms.DateField(
            label=_('تاريخ الفاتورة'),
            widget=forms.DateInput(
                # attrs={"type": "Date", "max": datetime.date.today(),}
                attrs={"type": "Date",}
            ),
            initial=datetime.date.today(),
        )
    
        # self.fields['branch'] = forms.ModelChoiceField(queryset=branches, required=True)
        self.fields["store"] = forms.ModelChoiceField(
            label=_('المخزن'),
            queryset=Store.objects.all(), required=False
        )
        self.fields["store"].widget.attrs.update(
            {"class": " store select form-control"}
            )
        try:

            try:
                general_var = None
            except ObjectDoesNotExist as e:
                pass

            self.fields["statement"].widget.attrs.update({"class": "form-control"})
            self.fields["reference_number"].widget.attrs.update(
                {"class": "form-control"}
            )
            self.fields["code"].widget.attrs.update({"class": "   form-control"})
            self.fields["date"].widget.attrs.update({"class": "   form-control"})
            self.fields["customer"].widget.attrs.update({"class": "   form-control"})
            self.fields["tax"].widget.attrs.update({"class": "   form-control"})
            # self.fields["due_date"].widget.attrs.update({"class": "   form-control"})
            self.fields["check_amount"].widget.attrs.update({"class": "   form-control"})
            self.fields["statement"].widget.attrs.update({"class": "   form-control"})
            self.fields["reference_number"].widget.attrs.update({"class": "   form-control"})
            self.fields["total_amount"].widget.attrs.update({"class": "   form-control"})
            self.fields["discount"].widget.attrs.update({"class": "   form-control"})
            self.fields["discount_rate"].widget.attrs.update({"class": "   form-control"})

        except ObjectDoesNotExist as e:

            raise e

    class Meta:
        model = SalesInvoicelocal
        fields = [
            "code",
            "date",
            "customer",
            "tax",
            "check_amount",
           
            "amount",
            "statement",
            "reference_number",
            "total_amount",
            "discount",
            "discount_rate",
            'is_stage',
        ]
       
        widgets = {
            "statement": forms.Textarea(attrs={"rows": 1, "class": "form-control","required":False}),
            "store": forms.Select(),
            "discount": forms.NumberInput(
                attrs={"class": "form-control", "oninput": "getPercentag(this)"}
            ),
            "discount_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "oninput": "getPercentag(this)",
                    "min": "0",
                    "max": "100",
                }
            ),
            "code": forms.NumberInput(attrs={"readonly": True}),
            "total_amount": forms.NumberInput(
                attrs={"class": "form-control", "readonly": True}
            ),
            "tax": forms.NumberInput(attrs={"class": "form-control", "readonly": True}),
        }
        labels = {
            "total_amount": _("المجموع"),
            "code": _("رقم الفاتورة"),
            "discount": _("تخفيض"),
            "discount_rate": _("تخفيض %"),
            "total_net_bill": _("إجمالي بعد الخصم"),

            "tax": _("الضريبة"),
        }


class SalesInvoicelocalDetailsForm(forms.ModelForm):
    """Form For Sales Invoicelocal Details
    """
    

    def __init__(self, *args, **kwargs):
        super(SalesInvoicelocalDetailsForm, self).__init__(*args, **kwargs)
        self.fields["item"] = forms.ModelChoiceField(
            label="",
            queryset=Items.objects.all(),

        )
        self.fields["unit"].widget.attrs.update(
                {
                    "class": "formset-field form-control",
                    "onchange":"get_store_items_data(this)",
                }
            )

        self.fields["total_price"] = forms.FloatField(
            label="",
            required=False,
            widget=forms.NumberInput(
                attrs={
                    "oninput": "getPrice(this)",
                    "readonly": True,
                    "class": "formset-field form-control sss",
                    "style": "width: 150px !important",
                }
            ),
        )
        # self.fields["expire_date"] = forms.ChoiceField(
        #     label="",
        #     required=True,
        
        # )
        # self.fields["expire_date"].widget.attrs.update(
        #         {
        #             "class": "formset-field form-control",
        #             "onchange":"get_store_items_data(this)",
                    
        #         }
        #     )

        # try:
        #     general_var = None

        # except ObjectDoesNotExist as e:
        #     pass
        try:
            attrs = {}
            self.fields["item"].widget.attrs.update(
                {
                    "class": "formset-field form-control",
                    "style": "width: 150px !important",
                    "onchange": "get_Price_item(this)",
                    "required": True,
                }
            )
           
            # show_statement_item_level
            
            self.fields["statement"].widget.attrs.update({"required": False})
            del self.fields["statement"]

          
            self.fields["item_specification"].widget.attrs.update(
                {"required": False}
            )
            del self.fields["item_specification"]

            
            ITEM_DISCOUNT_TYPE =""
            if ITEM_DISCOUNT_TYPE == "Percentage":
                self.fields["discount"].widget.attrs.update(
                    {"required": False, "readonly": True}
                )

            elif ITEM_DISCOUNT_TYPE == "Amount":
                self.fields["discount_rate"].widget.attrs.update({"readonly": True,"style": "width: 100px !important",})

            else:
                pass
            self.fields["selling_price"].widget.attrs.update({"required": False})
            del self.fields["selling_price"]
        except:
            pass


    qty_store = forms.IntegerField(
        label="",
        widget=forms.NumberInput(attrs={"class": "formset-field form-control","readonly": True,"style": "width: 100px !important"})
    )

    class Meta:
        model = SalesInvoicelocalDetails

        fields = [
            "item",
            "unit",
            "qty",
            # "expire_date",
            "statement",
            "discount",
            "discount_rate",
            "store",
            "selling_price",
            
        ]

        widgets = {
            "qty_store":forms.NumberInput(
                attrs={
                    "class": "formset-field form-control sss",
                    "style": "width: 100px !important",
                }
            ),
            "total_price": forms.NumberInput(
                attrs={
                    "class": "formset-field form-control sss",
                    "style": "width: 100px !important",
                }
            ),
            "qty": forms.NumberInput(
                attrs={
                    "class": "formset-field form-control sss",
                    "step": 1,
                    "oninput": "getTotal(this)",
                    "style": "width: 100px !important",
                }
            ),
            "unit": forms.Select(
                attrs={
                    "class": "formset-field form-control sss",
                    "style": "width: 100px !important",
                }
            ),
            "store": forms.Select(
                attrs={
                    "class": " formset-field form-control sss",
                    "style": "width: 100px !important",
                }
            ),
    
            # "expire_date": forms.DateInput(
            #     attrs={
            #         "class": "formset-field form-control sss",
            #         "type": "date",
            #         "onclick": "chake_date(this)",
            #         "style": "width: 100px !important",
            #     }
            # ),
            "statement": forms.TextInput(
                attrs={
                    "class": "formset-field form-control sss",
                    "style": "width: 100px !important",
                }
            ),
            "discount": forms.NumberInput(
                attrs={
                    "class": "sss formset-field form-control",
                    "oninput": "getTotal(this)",
                    "style": "width: 100px !important",
                }
            ),
       
            "discount_rate": forms.NumberInput(
                attrs={
                    "class": "sss formset-field form-control",
                    "style": "width: 150px !important",
                    "oninput": "getTotal(this)",
                    "min": "0",
                    "max": "100",
                }
            ),
            "selling_price": forms.NumberInput(
                attrs={
                    "class": "sss formset-field form-control",
                    "style": "width: 100px !important",
                }
            ),
        }
        labels = {
            "total_price": "",
            "item": "",
            "unit": "",
            "qty": "",
            "expire_date": "",
            "statement": "",
            "discount": "",
            "discount_rate": "",
            "store": "",
            "selling_price": "",
            "item_specification": "",
        }
