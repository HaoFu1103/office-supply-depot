from .models import Order
from django.contrib.auth.models import User
from django.shortcuts import render
from django import forms
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator

    # full_name = forms.CharField(max_length=100, required=True)

class addressForm(forms.Form):
    # full_name = forms.CharField(max_length=100, required=True)
    street_address = forms.CharField(label='Street address', max_length=150, required=True)
    apt_suite_other = forms.CharField(label='Apt / Suite / Other',max_length=150, required=False)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=2, required=True, help_text= 'eg. CA')
    zip = forms.CharField(max_length=5, required=True)
    credit_card_number = forms.CharField(label='Credit Card Number', max_length=12, min_length=12, required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+', 'title':'Enter numbers Only '}))

    #class Meta:
    #    model = Order
    #    fields = ('ship_address',)


