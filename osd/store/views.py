from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category,Product

def index(request):
    text = 'First django app'
    return HttpResponse(text)

#Category view
def allProdCat(request, c_slug=None):
    c_page = None
    products = None
    if c_slug!=None:
        c_page = get_object_or_404(Category,slug=c_slug)
        products = Product.objects.filter(category=c_page,available=True)
    else:
        products= Product.objects.all().filter(available=True)
    return render(request,'store/category.html',{'category':c_page,'products':products})
