from django.shortcuts import render, get_object_or_404
from .models import Order
from .forms import addressForm
# Create your views here.
def thanks(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
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
