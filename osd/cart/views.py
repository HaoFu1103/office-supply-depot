from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from order.models import Order, OrderDetail

from order.forms import addressForm


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save(),
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart
        )
        cart_item.save()
    return redirect('cart:cart_detail')

def cart_detail(request, total=0, counter=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    return render(request, 'cart.html', dict(cart_items = cart_items, total = total, counter = counter))

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')

def check_out(request, overallTotal=0, costTotal=0, weightTotal=0, counter=0, cart_items = None, deliveryCost1=0, deliveryCost2=0):
    if request.method == 'GET':
        form = addressForm()
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            costTotal += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
        for cart_item in cart_items:
            weightTotal += (cart_item.product.weight * cart_item.quantity)
            counter += cart_item.quantity
        if costTotal <= 100 and weightTotal <= 15:
            deliveryCost1 = 20
        elif costTotal <= 100 and weightTotal > 15:
            deliveryCost2 = 20
        else:
            deliveryCost1 = 0
            deliveryCost2 = 0
        overallTotal = costTotal + deliveryCost1
    except ObjectDoesNotExist:
        pass
    if request.method == 'POST':
        form = addressForm(request.POST)
        if form.is_valid:
            data = request.POST.copy()
            shipping_address = data.get('street_address') + ' ' + data.get('apt_suite_other') + ', ' + data.get('city') + ', ' + data.get('state') + data.get('zip')
            try:
                try:
                    current_order = Order.objects.create(
                        total = overallTotal,
                        ship_address = shipping_address
                    )
                    for order_item in cart_items:
                        order_detail = OrderDetail.objects.create(
                            product = order_item.product.name,
                            quantity = order_item.quantity,
                            price = order_item.product.price,
                            order = current_order
                        )
                        order_detail.save()
                        # order stock reduced on order save
                        products = Product.objects.get(id=order_item.product.id)
                        products.stock = int(order_item.product.stock - order_item.quantity)
                        products.save()
                        order_item.delete()
                    request.session['order_id'] = current_order.order_id
                    return redirect('order:thanks')
                except ObjectDoesNotExist:
                    pass
            except Exception as e:
                return False, e
    return render(request, 'checkout.html', dict(form = form, cart_items = cart_items, overallTotal=overallTotal, costTotal = costTotal, weightTotal = weightTotal, counter = counter, deliveryCost1=deliveryCost1, deliveryCost2=deliveryCost2))
