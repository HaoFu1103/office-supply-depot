from .models import Order
from django.contrib.auth.models import User
from django.shortcuts import render
from django import forms
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError


    # full_name = forms.CharField(max_length=100, required=True)

class addressForm(forms.Form):
    # full_name = forms.CharField(max_length=100, required=True)
    street_address = forms.CharField(label='Street address', max_length=150, required=True)
    apt_suite_other = forms.CharField(label='Apt / Suite / Other',max_length=150, required=False)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=2, required=True, help_text= 'eg. CA')
    zip = forms.CharField(max_length=5, required=True)
    numeric = RegexValidator(r'^[0-9]+', 'Must be numeric')
    # exp_date = RegexValidator(r'^[0-9]{2}/[0-9]{2}$')
    credit_card_number = forms.CharField(label='Credit Card Number', max_length=12, min_length=12, required=True, validators=[num_test])
    # cvv_number = forms.CharField(label='Credit Card CVV', max_length=3, min_length=3, required=True, validators=[numeric])
    # expiration_date = forms.CharField(label='Card Expiration (MM/YYYY)', required=True, validators=[exp_date])
    # class Meta:
    #     model = Order
    #     fields = ('ship_address',)

def num_test(val):
    if not re.match(r'[0-9]+', val):
        raise ValidationError('Must be numeric')
