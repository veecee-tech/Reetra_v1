from django import forms
from .models import Receipt_No, Item
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
import re



class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['receipt_no','item_name', 'item_price', 'item_qty', 'item_desc']
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args,**kwargs)    
        # self.fields['receipt_no'].queryset = Receipt_No.objects.filter(user_id = get_current_authenticated_user().id, is_submitted=False).order_by('-time_filter')
        # self.fields['receipt_no'].widget.attrs['style'] = "width: 100%;padding: 1.2rem;border: 1px solid var(--pc);border-radius: 3rem;color: var(--pc);font-size: 1.6rem;"
        self.fields['item_name'].widget.attrs['placeholder'] = 'Product Name'
        # self.fields['receipt_no'].widget.attrs['value']
        self.fields['item_price'].widget.attrs['placeholder'] = 'Product Price'
        self.fields['item_qty'].widget.attrs['placeholder'] = 'Product Quantity'  
        self.fields['item_desc'].widget.attrs['placeholder'] = 'Product Description'     


        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    
class GenerateReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt_No

        fields = ['receive_from', 'address', 'phone', 'currency_format']
       
    def clean_phone(self):
        
        phone = self.cleaned_data.get('phone')
    
        if not re.match(r'^([0]){1}([897]){1}([01]){1}[0-9]{8}$', phone):
            raise forms.ValidationError("Invalid Phone Number format")
        
        return phone

    def __init__(self, *args, **kwargs):
        super(GenerateReceiptForm, self).__init__(*args,**kwargs)
        # self.fields['receipt_no'].widget.attrs['name'] = "receipt_no"
        self.fields['receive_from'].widget.attrs['placeholder'] = "Customer's Name"
        self.fields['address'].widget.attrs['placeholder'] = "Customer's Address"
        self.fields['phone'].widget.attrs['placeholder'] = "Customer's Phone Number"
        self.fields['currency_format'].widget.attrs['placeholder'] = "Choose Your Desired Currency"
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UpdateItemForm(forms.ModelForm):
    
    class Meta:

        model = Item
    
        exclude = ['receipt_no']
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(UpdateItemForm, self).__init__(*args,**kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
  
