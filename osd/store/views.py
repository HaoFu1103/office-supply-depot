from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    text = 'First django app'
    return HttpResponse(text)
