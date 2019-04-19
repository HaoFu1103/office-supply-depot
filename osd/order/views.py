from django.shortcuts import render, get_object_or_404
from .models import Order
from .forms import addressForm
# Create your views here.
def thanks(request):
    print("IN order.views!!")
    order_id = request.session['order_id']
    if order_id:
        customer_order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'thanks.html', {'customer_order': customer_order})


def addressView(request):
    if request.method == 'POST':
        form = addressForm(request.POST)
        if form.is_valid():
            form.save()
            full_name = form.cleaned_data.get('full_name')
    else:
        form = addressForm()
    return render(request, 'thanks.html', {'form':form})
