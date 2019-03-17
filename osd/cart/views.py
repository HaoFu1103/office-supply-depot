from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from order.models import Order, OrderDetail


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
    if request.method == 'POST':
        try:
            # create variables for order information
            cus_id = request.POST['cus_id']
            ship_add = request.POST['ship_address']
            try:
                # create order
                order_details = Order.objects.create(
                    cus_id=cus_id,
                    ship_address=ship_add

                )
                for order_item in cart_items:
                    oi = OrderDetail.objects.create(
                        product=order_item.product.name,
                        quantity=order_item.quantity,
                        price=order_item.product.price,
                        order=order_details
                    )
                    oi.save()
                    # order stock reduced on order save
                    products = Product.objects.get(id=order_item.product.id)
                    products.stock = int(order_item.product.stock - order_item.quantity)
                    products.save()
                    order_item.delete()
                    print('The order has been created')
                return redirect('shop:allProdCat')
            except ObjectDoesNotExist:
                pass
        except Exception as e:
            return False, e
    # Process order information either here or on checkout
    # Ep 20 has information on adding order information to DB
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
