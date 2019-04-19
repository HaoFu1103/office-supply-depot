from order.models import Order
from django.contrib.auth.models import User
from django.shortcuts import render
from django import forms


class addressForm(forms.Form):
    # full_name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=150, required=True)
    # address_two = forms.CharField(max_length=150, required=False)
    # city = forms.CharField(max_length=100, required=True)
    # state = forms.CharField(max_length=2, required=True, help_text= 'eg. CA')
    # zip = forms.CharField(max_length=5, required=True)
    # class Meta:
    #     model = Order
    #     fields = ('ship_address',)
